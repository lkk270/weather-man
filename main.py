import asyncio
import logging
from datetime import datetime, timezone
from core.settings import LOCATIONS
from database.session import get_db_session
from providers.nws.forecast import (
    fetch_forecast_data,
    clean_forecast_data,
    load_forecast_data
)
from providers.nws.observation import (
    fetch_observation_data,
    clean_observation_data,
    load_observation_data
)
from alembic import command
from alembic.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def process_all_locations():
    """Process both forecast and observation data for all locations."""
    failed_locations = []

    for location_id in LOCATIONS:
        logger.info(
            f"[Transaction Debug] Starting processing for location: {location_id}")
        try:
            async with get_db_session() as session:
                logger.info(
                    f"[Transaction Debug] Session created for {location_id}")
                try:
                    # Process forecast
                    raw_forecast = fetch_forecast_data(location_id)
                    cleaned_forecast = clean_forecast_data(
                        raw_forecast, location_id)
                    logger.info(
                        f"[Transaction Debug] About to load forecast data for {location_id}")
                    await load_forecast_data(cleaned_forecast, session)
                    await session.flush()
                    logger.info(
                        f"[Transaction Debug] Forecast data loaded for {location_id}")

                    # Process observation
                    raw_observation = fetch_observation_data(location_id)
                    cleaned_observation = clean_observation_data(
                        raw_observation, location_id)
                    logger.info(
                        f"[Transaction Debug] About to load observation data for {location_id}")
                    await load_observation_data(cleaned_observation, session)
                    await session.flush()
                    logger.info(
                        f"[Transaction Debug] Observation data loaded for {location_id}")

                except Exception as e:
                    logger.error(
                        f"[Transaction Debug] Inner transaction error for {location_id}: {str(e)}")
                    logger.error(
                        "Inner transaction stack trace:", exc_info=True)
                    raise

                logger.info(
                    f"[Transaction Debug] Transaction complete for {location_id}")

        except Exception as e:
            logger.error(
                f"[Transaction Debug] Outer session error for {location_id}: {str(e)}")
            logger.error("Outer session stack trace:", exc_info=True)
            failed_locations.append(location_id)

    if failed_locations:
        logger.error(
            f"Failed to process locations: {', '.join(failed_locations)}")
        return {
            'success': False,
            'failed_locations': failed_locations
        }

    return {'success': True}


def lambda_handler(event, context):
    """AWS Lambda entry point."""
    logger.info(f"Lambda triggered at {datetime.now(timezone.utc)}")
    logger.info(f"Event data: {event}")

    try:
        # Run migrations first
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")

        # Process locations using asyncio.run()
        result = asyncio.run(process_all_locations())

        if not result['success']:
            return {
                'statusCode': 500,
                'body': f'Pipeline failed for locations: {result["failed_locations"]}'
            }

        return {
            'statusCode': 200,
            'body': 'Weather pipeline completed successfully'
        }
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Pipeline failed: {str(e)}'
        }


if __name__ == "__main__":
    asyncio.run(process_all_locations())
