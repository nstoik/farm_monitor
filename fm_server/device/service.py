""" device service package """
import logging
import json
import pika

from fm_server.settings import get_config
from fm_database.base import get_session
from fm_database.models.device import Device

LOGGER = logging.getLogger('fm.device.service')

CONNECTED_DEVICES = {}
NEW_DEVICES = {}


class DeviceReceiver():
    """ communicate with devices via RabbitMQ """

    def __init__(self, logger):

        self.LOGGER = logger
        self.HEARTBEAT_RECEIVER = None
        self.DEVICE_MESSAGES = None

        # store and manage internal state
        self._connection = None
        self._channel = None
        self._closing = False

        config = get_config()

        # connection parameters
        self._user = config.RABBITMQ_USER
        self._password = config.RABBITMQ_PASSWORD
        self._host = config.RABBITMQ_HOST
        self._port = config.RABBITMQ_PORT
        self._virtual_host = config.RABBITMQ_VHOST

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """
        self.LOGGER.info('Connecting to RabbitMQ')

        creds = pika.PlainCredentials(self._user, self._password)
        params = pika.ConnectionParameters(host=self._host, port=self._port,
                                           virtual_host=self._virtual_host, credentials=creds)

        return pika.SelectConnection(parameters=params,
                                     on_open_callback=self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        self.LOGGER.debug('Connection opened')
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        self.LOGGER.debug('Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                                reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:

            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        self.LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        self.LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.HEARTBEAT_RECEIVER = HeartbeatReceiver(self._connection, self._channel)
        self.DEVICE_MESSAGES = DeviceMessages(self._connection, self._channel)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        self.LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self.LOGGER.warning('Channel %i was closed: (%s) %s',
                            channel, reply_code, reply_text)
        self._connection.close()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        self.LOGGER.debug('Closing the channel')
        self._channel.close()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        self.LOGGER.info('Closing connection')
        self._connection.close()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        self.LOGGER.info('Stopping')
        self._closing = True
        self.HEARTBEAT_RECEIVER.set_stopping(True)
        self.DEVICE_MESSAGES.set_stopping(True)
        self.HEARTBEAT_RECEIVER.stop_consuming()
        self.DEVICE_MESSAGES.start_consuming()
        self.close_channel()
        self._connection.ioloop.start()
        self.LOGGER.info('Stopped')


class HeartbeatReceiver():
    """ receive heartbeats """

    DEVICE_CONNECTION_INTERVAL = 10

    def __init__(self, connection, channel):

        self.LOGGER = logging.getLogger('fm.device.service.heartbeat')

        # store and manage internal state
        self._connection = connection
        self._channel = channel
        self._stopping = False
        self._consumer_tag = None

        self._session = get_session()

        config = get_config()

        self.exchange_name = config.RABBITMQ_HEARTBEAT_EXCHANGE_NAME
        self.exchange_type = config.RABBITMQ_HEARTBEAT_EXCHANGE_TYPE
        self.routing_key = config.RABBITMQ_HEARTBEAT_ROUTING_KEY
        self.queue_name = None

        self.setup_exchange(self.exchange_name)

    def set_stopping(self, state):
        """Set the _stopping state"""
        self._stopping = state

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        self.LOGGER.debug('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(callback=self.on_exchange_declareok,
                                       exchange=exchange_name,
                                       exchange_type=self.exchange_type)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        self.LOGGER.debug('Exchange declared')
        self.setup_queue()

    def setup_queue(self):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        self.LOGGER.debug('Declaring queue')
        self._channel.queue_declare(callback=self.on_queue_declareok,
                                    auto_delete=True,
                                    exclusive=True)

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self.queue_name = method_frame.method.queue
        LOGGER.info('Binding %s to %s with %s',
                    self.exchange_name, self.queue_name, self.routing_key)
        self._channel.queue_bind(callback=self.on_bindok,
                                 queue=self.queue_name,
                                 exchange=self.exchange_name,
                                 routing_key=self.routing_key)

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        self.LOGGER.debug('Queue bound')
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        self.LOGGER.debug('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(consumer_callback=self.on_message,
                                                         queue=self.queue_name)
        self.schedule_device_check()

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        self.LOGGER.debug('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        self.LOGGER.warning('Consumer was cancelled remotely, shutting down: %r',
                            method_frame)
        if self._channel:
            self._channel.close()

    def schedule_device_check(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        device check.

        """
        if self._stopping:
            return
        self._connection.add_timeout(self.DEVICE_CONNECTION_INTERVAL,
                                     self.device_check)

    def device_check(self):
        """Check if a device is 'dead' or not"""
        for device in CONNECTED_DEVICES.copy().values():
            device.heartbeat()
            if not device.is_alive():
                self._session.query(Device).filter_by(id=device.device_id) \
                                           .update({Device.connected: False})
                self._session.commit()
                self.LOGGER.info(f'{device.device_id} is no longer connected')
                del CONNECTED_DEVICES[device.device_id]

        for device in NEW_DEVICES.copy().values():
            device.heartbeat()
            if not device.is_alive():
                self._session.query(Device).filter_by(id=device.device_id) \
                                           .update({Device.connected: False})
                self._session.commit()
                self.LOGGER.info(f'{device.device_id} is no longer connected')
                del NEW_DEVICES[device.device_id]

        self.schedule_device_check()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        self.LOGGER.debug('Received message # %s from %s',
                     basic_deliver.delivery_tag, properties.app_id)

        payload = json.loads(body)

        device_id = properties.app_id
        if device_id in CONNECTED_DEVICES:
            CONNECTED_DEVICES[device_id].on_message_received()
            return_message = 'connected'
        else:
            return_message = self.on_new_device(device_id)

        self.acknowledge_message(basic_deliver.delivery_tag)

        reply_properties = pika.BasicProperties(correlation_id=properties.correlation_id)
        self._channel.basic_publish(exchange='',
                                    routing_key=properties.reply_to,
                                    properties=reply_properties,
                                    body=return_message)

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        self.LOGGER.debug('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def on_new_device(self, device_id):
        """Check if device has been configured or not when a new device connects"""

        device = self._session.query(Device).filter_by(id=device_id).first()

        if not device:
            # device has not been added to the db but has been seen before
            if device_id in NEW_DEVICES:
                NEW_DEVICES[device_id].on_message_received()
            # device has not been added to the db and hasn't been seen before
            else:
                self.LOGGER.info(f'{device_id} connected. Has not been configured yet.')
                NEW_DEVICES[device_id] = DeviceRep(device_id)
            return 'new'
        else:
            # device has been added to the db but was currently a NEW_DEVICE
            if device_id in NEW_DEVICES:
                self.LOGGER.info(f'{device_id} now connected.')
                device_object = NEW_DEVICES.pop(device_id)
                device_object.on_message_received()
                CONNECTED_DEVICES[device_id] = device_object
            # device has been added to the db but has not been seen yet
            else:
                self.LOGGER.info(f'{device_id} connected.')
                CONNECTED_DEVICES[device_id] = DeviceRep(device_id)
            device.connected = True
            self._session.commit()
            return 'connected'

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        self._session.close()

        if self._channel:
            self.LOGGER.debug('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        self.LOGGER.debug('RabbitMQ acknowledged the cancellation of the consumer')


class DeviceMessages():
    """ receive and respond to internal message requests """

    def __init__(self, connection, channel):

        self.LOGGER = logging.getLogger('fm.device.service.messages')

        # store and manage internal state
        self._connection = connection
        self._channel = channel
        self._stopping = False
        self._consumer_tag = None

        config = get_config()

        self.exchange_name = config.RABBITMQ_MESSAGES_EXCHANGE_NAME
        self.exchange_type = config.RABBITMQ_MESSAGES_EXCHANGE_TYPE
        self.routing_key = '_internal'
        self.queue_name = None

        self.setup_exchange(self.exchange_name)

    def set_stopping(self, state):
        """Set the _stopping state"""
        self._stopping = state

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        self.LOGGER.debug('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(callback=self.on_exchange_declareok,
                                       exchange=exchange_name,
                                       exchange_type=self.exchange_type)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        self.LOGGER.debug('Exchange declared')
        self.setup_queue()

    def setup_queue(self):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        self.LOGGER.debug('Declaring queue')
        self._channel.queue_declare(callback=self.on_queue_declareok,
                                    auto_delete=True,
                                    exclusive=True)

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self.queue_name = method_frame.method.queue
        LOGGER.info('Binding %s to %s with %s',
                    self.exchange_name, self.queue_name, self.routing_key)
        self._channel.queue_bind(callback=self.on_bindok,
                                 queue=self.queue_name,
                                 exchange=self.exchange_name,
                                 routing_key=self.routing_key)

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        self.LOGGER.debug('Queue bound')
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        self.LOGGER.debug('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(consumer_callback=self.on_message,
                                                         queue=self.queue_name)

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        self.LOGGER.debug('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        self.LOGGER.warning('Consumer was cancelled remotely, shutting down: %r',
                            method_frame)
        if self._channel:
            self._channel.close()


    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """

        payload = json.loads(body)
        command = payload['command']
        device_id = payload['id']
        return_message = 'done'

        LOGGER.debug(f'Received request {command} for {device_id}')

        if command == 'device_status':
            if device_id in NEW_DEVICES:
                return_message = 'new'
            elif device_id in CONNECTED_DEVICES:
                return_message = 'connected'
            else:
                return_message = 'disconnected'
        else:
            return_message = 'unknown command'

        self.acknowledge_message(basic_deliver.delivery_tag)

        reply_properties = pika.BasicProperties()
        self._channel.basic_publish(exchange='',
                                    routing_key=properties.reply_to,
                                    properties=reply_properties,
                                    body=return_message)

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        self.LOGGER.debug('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.
        """
        if self._channel:
            self.LOGGER.debug('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        self.LOGGER.debug('RabbitMQ acknowledged the cancellation of the consumer')


class DeviceRep(object):
    """
    Helper class to represent a device to a worker
    """
    HEARTBEAT_LIVES = 3

    def __init__(self, device_id):
        self.device_id = device_id
        self.lives = self.HEARTBEAT_LIVES
        return

    def heartbeat(self):
        """decrease live count by 1"""
        if self.lives > 0:
            self.lives -= 1
        return

    def on_message_received(self):
        """set live count to max when message received"""
        self.lives = self.HEARTBEAT_LIVES
        return

    def is_alive(self):
        """is device still alive?"""
        return self.lives > 0


def run_device():
    """ run the device receiver """
    device_receiver = DeviceReceiver(logger=LOGGER)

    try:
        device_receiver.run()
    except KeyboardInterrupt:
        LOGGER.info("Stopping device receiver")
        device_receiver.stop()
