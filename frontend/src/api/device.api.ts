import Request from "@/api/fetch";
import { Device, DeviceUpdate } from "@/interfaces/device.interface";
import { PaginationHeader } from "@/interfaces/fetch.interface";

export class DeviceRequest extends Request {
  constructor() {
    super();
    this.resourceLocation = `${this.baseURL}device/`;
  }

  public async getDevices(): Promise<Array<Device>> {
    const url = `${this.resourceLocation}`;
    return this.client.get(url).then((response) => {
      // convert any dates from strings to Date objects.
      // Add the timezone offset to the date to make it local time.
      response.data.forEach((device: Device) => {
        device.lastUpdateReceived = new Date(device.lastUpdateReceived + "Z");
        device.lastUpdated = new Date(device.lastUpdated + "Z");
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
    // Add the timezone offset to the date to make it local time.
    deviceUpdates.forEach((deviceUpdate: DeviceUpdate) => {
      deviceUpdate.timestamp = new Date(deviceUpdate.timestamp + "Z");
    });
    return [deviceUpdates, paginationHeader];
  }
}
