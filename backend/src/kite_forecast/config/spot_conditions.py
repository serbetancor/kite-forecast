from kite_forecast.models.spot_conditions import (
    SpotConditions,
    WaveConditions,
    WaveScoreWeights,
    WindConditions,
    WindScoreWeights,
)

SPOT_CONDITIONS: tuple[SpotConditions, ...] = (
    # Valores iniciales orientativos, pendientes de calibración con datos reales.
    # Las referencias del spot indican aproximadamente 15–30 kt en invierno
    # y 20–35+ kt en verano. El rango adecuado depende también del rider
    # y del material; estos valores no son límites de seguridad.
    SpotConditions(
        beach_id="salinas",
        wind=WindConditions(
            preferred_directions_deg=(0.0, 22.5, 45.0),
            direction_tolerance_deg=22.5,
            min_speed_knots=15.0,
            ideal_speed_knots=25.0,
            max_speed_knots=35.0,
            max_gust_knots=35.0,
            score_weights=WindScoreWeights(
                speed=0.5,
                direction=0.3,
                gusts=0.2,
            ),
        ),
        waves=WaveConditions(
            preferred_directions_deg=(60.0,),
            direction_tolerance_deg=30.0,
            min_height_m=0.0,
            ideal_height_m=1.0,
            max_height_m=2.5,
            min_period_s=5.0,
            score_weights=WaveScoreWeights(
                height=0.5,
                period=0.3,
                direction=0.2,
            ),
        ),
    ),
)
