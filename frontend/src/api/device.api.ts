import Request from "@/api/fetch";
import { Device } from "@/interfaces/device.interface";

export class DeviceRequest extends Request {
  constructor() {
    super();
    this.resourceLocation = `${this.baseURL}devices/`;
  }

  public async getDevices(): Promise<Array<Device>> {
    const url = `${this.resourceLocation}`;
    return this.client.get(url).then((response) => {
      // convert any dates from strings to Date objects
      response.data.forEach((device: Device) => {
        device.lastUpdateReceived = new Date(device.lastUpdateReceived);
        device.lastUpdated = new Date(device.lastUpdated);
      });
      return response.data;
    });
  }
}
