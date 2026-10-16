import type { BeachOption } from "../models/config"
import type { OpenMeteoResponse, WeeklyBeachForecast } from "../models/response"
import { getWeeklyDateRange } from "../utils/getters"
import {
  fetchOpenMeteo,
  MARINE_API_URL,
  WEATHER_API_URL,
} from "./forecastService"

export async function loadWeeklyForecasts(
  beaches: BeachOption[],
): Promise<WeeklyBeachForecast[]> {
  const { startDate, endDate } = getWeeklyDateRange()

  return Promise.all(
    beaches.map(async (beach) => {
      const [weather, marine] = await Promise.all([
        fetchOpenMeteo<OpenMeteoResponse>(
          WEATHER_API_URL,
          beach,
          endDate,
          startDate,
        ),
        fetchOpenMeteo<OpenMeteoResponse>(
          MARINE_API_URL,
          beach,
          endDate,
          startDate,
        ),
      ])

      return {
        beach_id: beach.id,
        weather,
        marine,
      }
    }),
  )
}
