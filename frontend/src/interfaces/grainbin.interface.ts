export type Grainbin = {
  averageTemp: string;
  userConfigured: boolean;
  busNumber: number;
  lastUpdated: Date;
  device: number;
  name: string;
  sensorType: string;
  totalUpdates: number;
  description: string;
  id: number;
  url: string;
  busNumberString: string;
  grainbinType: string;
};

export type GrainbinUpdate = {
  id: number;
  // cable number
  temphigh: number;
  // sensor number
  templow: number;
  timestamp: Date;
  grainbin: number;
  updateIndex: number;
  sensorName: string;
  temperature: number;
};
