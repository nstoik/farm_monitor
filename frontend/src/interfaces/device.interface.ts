export type Device = {
  location: string;
  lastUpdateReceived: Date;
  deviceId: string;
  hardwareVersion: string;
  connected: boolean;
  userConfigured: boolean;
  url: string;
  description: string;
  name: string;
  totalUpdates: number;
  grainbinCount: number;
  lastUpdated: Date;
  softwareVersion: string;
};
