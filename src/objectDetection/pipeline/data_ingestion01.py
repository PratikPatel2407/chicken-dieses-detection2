from objectDetection.entity.config_entity import DataIngestionConfig
from objectDetection.config.configuration import configurationManager
from objectDetection import logger
from objectDetection.components.data_ingestion import DataIngestion




STAGE_NAME = "Data ingestion Stage"

class DataIngestionTrainingPipieline:
    def __init__(self):
        pass

    def main(self):
        config = configurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()




if __name__ =="__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<<<<")
        obj = DataIngestionTrainingPipieline()
        obj.main()
        logger.info(f">>>>>>> {STAGE_NAME}  complted <<<<<")
    except Exception as e:
        logger.exception(e)
        raise e