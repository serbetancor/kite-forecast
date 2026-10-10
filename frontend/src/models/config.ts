export interface BeachOption {
  id: string
  name: string
}

export interface AppConfig {
  forecast_horizon_days: number
  beaches: BeachOption[]
}
