export interface Beach {
  id: string
  name: string
  location: {
    latitude: number
    longitude: number
  }
}

export interface WeatherReport {
  temperature_c: number
}

export interface WavesReport {
  height_m: number
  direction_deg: number
  direction_cardinal: string
  period_s: number
}

export interface SeaReport {
  level_m: number
  current_velocity_kmh: number
  current_direction_deg: number
  current_direction_cardinal: string
}

export interface WindReport {
  speed_kmh: number
  direction_deg: number
  direction_cardinal: string
  gusts_kmh: number
}

export interface WindScoreReport {
  total: number
  speed: number
  direction: number
  gusts: number
}

export interface WavesScoreReport {
  total: number
  height: number
  period: number
  direction: number
}

export interface ScoreReport {
  total: number
  wind: WindScoreReport
  waves: WavesScoreReport
}

export interface ScoredHour {
  beach_id: string
  datetime: string
  score: ScoreReport
}
export interface ObjectiveReport {
  beach: Beach
  timestamp: string
  wind: WindReport
  weather: WeatherReport
  waves: WavesReport
  sea: SeaReport
  score: ScoreReport
}

export interface KiteSizingCell {
  weight_kg: number
  kite_size_m2: number
  score: number
}

export interface KiteSizingMatrix {
  timestamp: string
  wind_speed_kmh: number
  wind_gusts_kmh: number
  weights_kg: number[]
  kite_sizes_m2: number[]
  cells: KiteSizingCell[]
}
