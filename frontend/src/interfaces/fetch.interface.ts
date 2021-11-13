import { DeviceRequest } from "@/api/device.api";
import { Device } from "./device.interface";

export type PaginationHeader = {
  total: number;
  totalPages: number;
  firstPage: number;
  lastPage: number;
  page: number;
};

export type APIRequestObject = DeviceRequest;

export type APIRequestType = Device;

// export type APIRequestObject = UserRequest | AppointmentRequest;

// export type APIRequestType = User | Appointment;
