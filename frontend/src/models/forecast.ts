export interface Beach {
  id: string;
  name: string;
  location: {
    latitude: number;
    longitude: number;
  };
}

export interface WeatherReport {
  temperature_c: number;
}

export interface WavesReport {
  height_m: number;
  direction_deg: number;
  direction_cardinal: string;
  period_s: number;
}

export interface SeaReport {
  level_m: number;
  current_velocity_kmh: number;
  current_direction_deg: number;
  current_direction_cardinal: string;
}

export interface WindReport {
  speed_knots: number;
  direction_deg: number;
  direction_cardinal: string;
  gusts_knots: number;
}

export interface ObjectiveReport {
  beach: Beach;
  timestamp: string;
  wind: WindReport;
  weather: WeatherReport;
  waves: WavesReport;
  sea: SeaReport;
}
