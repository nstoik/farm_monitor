import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import DeviceCard from '@/components/device/DeviceCard.vue'
import { type Device } from '@/interfaces/device.interface'

const device: Device = {
  id: 1,
  location: 'Location',
  lastUpdateReceived: new Date(),
  deviceId: 'Device ID',
  hardwareVersion: 'Hardware Version',
  connected: true,
  userConfigured: true,
  url: '/device/1/',
  description: 'Description',
  name: 'Device 1',
  totalUpdates: 0,
  grainbinCount: 0,
  lastUpdated: new Date(),
  softwareVersion: 'Software Version'
}

describe('DeviceCard', () => {
  it('renders properly', () => {
    const wrapper = mount(DeviceCard, {
      props: {
        device: device
      }
    })
    expect(wrapper.text()).toContain('Device 1')
    expect(wrapper.find('div.card-footer').text()).toContain('Last Update:')
  })
})
