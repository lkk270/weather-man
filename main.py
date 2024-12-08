import asyncio
import logging
import requests
import sys
from datetime import datetime, timezone
from core.settings import LOCATIONS
from database import SessionLocal
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


async def process_location_forecast(location_id: str):
    """Process forecast data for a single location."""
    try:
        logger.info(f"Fetching forecast data for {location_id}")
        raw_data = fetch_forecast_data(location_id)

        logger.info(f"Cleaning forecast data for {location_id}")
        cleaned_data = clean_forecast_data(raw_data, location_id)

        logger.info(
            f"Loading {len(cleaned_data)} forecast records for {location_id}")
        await load_forecast_data(cleaned_data)

        logger.info(f"Successfully processed forecast data for {location_id}")
    except Exception as e:
        logger.error(f"Error processing forecast for {location_id}: {str(e)}")
        raise


async def process_location_observation(location_id: str):
    """Process observation data for a single location."""
    try:
        logger.info(f"Fetching observation data for {location_id}")
        raw_data = fetch_observation_data(location_id)

        logger.info(f"Cleaning observation data for {location_id}")
        cleaned_data = clean_observation_data(raw_data, location_id)

        logger.info(f"Loading observation data for {location_id}")
        records_added = await load_observation_data(cleaned_data)

        logger.info(
            f"Successfully loaded {records_added} new observations for {location_id}")
    except Exception as e:
        logger.error(
            f"Error processing observations for {location_id}: {str(e)}")
        raise


async def process_all_locations():
    """Process both forecast and observation data for all locations."""
    async with SessionLocal() as session:
        async with session.begin():
            try:
                for location_id in LOCATIONS:
                    logger.info(f"Processing location: {location_id}")

                    # Process forecast
                    raw_forecast = fetch_forecast_data(location_id)
                    cleaned_forecast = clean_forecast_data(
                        raw_forecast, location_id)
                    await load_forecast_data(cleaned_forecast, session)

                    # Process observation
                    raw_observation = fetch_observation_data(location_id)
                    cleaned_observation = clean_observation_data(
                        raw_observation, location_id)
                    await load_observation_data(cleaned_observation, session)

                    logger.info(f"Completed processing for {location_id}")

            except Exception as e:
                logger.error(f"Error in process_all_locations: {str(e)}")
                raise


def main():
    """Main entry point for the weather data pipeline."""
    try:
        logger.info("Starting weather data pipeline")
        asyncio.run(process_all_locations())
        logger.info("Weather data pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise


async def lambda_handler(event, context):
    """AWS Lambda entry point."""
    logger.info(f"Lambda triggered at {datetime.now(timezone.utc)}")
    logger.info(f"Event data: {event}")

    try:
        # Run migrations first
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")

        # Process locations
        await process_all_locations()

        return {
            'statusCode': 200,
            'body': 'Weather pipeline completed successfully'
        }
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
