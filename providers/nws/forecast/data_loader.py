from datetime import datetime, timezone
from sqlalchemy import func, select, desc
from database.models import WeatherForecast
import logging

logger = logging.getLogger(__name__)


async def load_forecast_data(data, session):
    logger.info("Starting load_forecast_data")
    if not data:
        logger.info("No data provided to load_forecast_data")
        return 0

    return await _load_forecast_data(data, session)


async def _load_forecast_data(data, session):
    try:
        location = data[0]["location"]
        logger.info(
            f"[Transaction Debug] Starting forecast load for {location}")

        current_time = datetime.now(timezone.utc)
        for record in data:
            record['created_at'] = current_time
            forecast = WeatherForecast(**record)
            session.add(forecast)
            logger.debug(
                f"[Transaction Debug] Added forecast record for {location}")

        logger.info(f"[Transaction Debug] About to flush {len(data)} records")
        await session.flush()
        logger.info(f"[Transaction Debug] Flush complete for {location}")
        return len(data)
    except Exception as e:
        logger.error(
            f"[Transaction Debug] Error in _load_forecast_data: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        raise
