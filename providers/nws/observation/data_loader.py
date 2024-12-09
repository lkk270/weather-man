import logging
from datetime import datetime, timezone
from sqlalchemy import func, select, desc
from database.models import WeatherObservation

logger = logging.getLogger(__name__)


async def load_observation_data(data, session):
    logger.info("[Transaction Debug] Starting load_observation_data")
    if not data:
        logger.info("[Transaction Debug] No data provided")
        return 0

    return await _load_observation_data(data, session)


async def _load_observation_data(data, session):
    try:
        location = data[0]["location"]
        logger.info(
            f"[Transaction Debug] Starting observation load for {location}")

        latest_observation_query = (
            select(WeatherObservation.observed_time)
            .where(WeatherObservation.location == location)
            .order_by(desc(WeatherObservation.observed_time))
            .limit(1)
        )

        result = await session.execute(latest_observation_query)
        latest_time = result.scalar()

        new_records = []
        if latest_time:
            print(
                f"Latest observation in DB for {location} was at: {latest_time}")
            new_records = [
                record for record in data
                if record["observed_time"] > latest_time
            ]
        else:
            print(
                f"No existing observations found for {location}, will load all records")
            new_records = data

        if not new_records:
            print("No new observations to load")
            return 0

        print(
            f"Found {len(new_records)} new observations to load for {location}")

        current_time = datetime.now(timezone.utc)
        for record in new_records:
            record['created_at'] = current_time
            observation = WeatherObservation(**record)
            session.add(observation)

        await session.flush()
        logger.info(
            f"[Transaction Debug] Flush complete for {location}")
        return len(new_records)
    except Exception as e:
        logger.error(
            f"[Transaction Debug] Error in _load_observation_data: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        raise
