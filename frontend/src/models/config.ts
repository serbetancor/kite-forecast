export interface BeachOption {
  id: string
  name: string
  latitude: number
  longitude: number
}

export interface AppConfig {
  forecast_horizon_days: number
  beaches: BeachOption[]
}
