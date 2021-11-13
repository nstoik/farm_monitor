import Request from "@/api/fetch";
import { Device } from "@/interfaces/device.interface"

export class DeviceRequest extends Request {
  constructor() {
    super();
    this.resourceLocation = `${this.baseURL}devices`;
  }

  public async getDevices(): Promise<Array<Device>> {
      const url = `${this.resourceLocation}`;
      return this.client.get(url).then(response => response.data);
  }

}

export default new DeviceRequest();