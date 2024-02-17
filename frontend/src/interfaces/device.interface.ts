export type Device = {
  id: number
  location: string
  lastUpdateReceived: Date
  deviceId: string
  hardwareVersion: string
  connected: boolean
  userConfigured: boolean
  url: string
  description: string
  name: string
  totalUpdates: number
  grainbinCount: number
  lastUpdated: Date
  softwareVersion: string
}

export type DeviceUpdate = {
  deviceTemp: number
  diskFree: number
  diskTotal: number
  interiorTemp: number
  timestamp: Date
  exteriorTemp: number
  updateIndex: number
  uptime: number
  loadAvg: number
  diskUsed: number
  device: number
}
