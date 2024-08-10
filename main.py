from objectDetection import logger
from objectDetection.pipeline.data_ingestion01 import DataIngestionTrainingPipieline




STAGE_NAME = "Data ingestion Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<<<<")
    data_ingestion  = DataIngestionTrainingPipieline()
    data_ingestion.main()
    logger.info(f">>>>>>> {STAGE_NAME}  complted <<<<<")
except Exception as e:
    logger.exception(e)
    raise e