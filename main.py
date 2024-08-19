from objectDetection import logger
from objectDetection.pipeline.data_ingestion01 import DataIngestionTrainingPipieline
from objectDetection.pipeline.prepare_base_model02 import PrepareBaseModelTrainingPipeline




STAGE_NAME = "Data ingestion Stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<<<<")
    data_ingestion  = DataIngestionTrainingPipieline()
    data_ingestion.main()
    logger.info(f">>>>>>> {STAGE_NAME}  complted <<<<<")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Prepare base Model"

try:
    logger.info(f"*****************")
    logger.info(f">>>>>>>> stage {STAGE_NAME} started")
    prepare_base_model= PrepareBaseModelTrainingPipeline()
    prepare_base_model.main()
    logger.info(f">>>>>>>> stag{STAGE_NAME} complted")
except Exception as e:
        logger.exception(e)
        raise  e