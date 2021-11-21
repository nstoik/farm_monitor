import Request from "@/api/fetch";
import { Device, DeviceUpdate } from "@/interfaces/device.interface";
import { PaginationHeader } from "@/interfaces/fetch.interface";

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

  public async getDeviceUpdates(
    id: number,
    page = 1,
    pageSize = 10
  ): Promise<[Array<DeviceUpdate>, PaginationHeader]> {
    const url = `${this.resourceLocation}${id}/updates`;
    const [deviceUpdates, paginationHeader] =
      await this.getPaginate<DeviceUpdate>(url, page, pageSize).then(
        (response) => response
      );

    // convert any dates from strings to Date objects
    deviceUpdates.forEach((deviceUpdate: DeviceUpdate) => {
      deviceUpdate.timestamp = new Date(deviceUpdate.timestamp);
    });
    return [deviceUpdates, paginationHeader];
  }
}
