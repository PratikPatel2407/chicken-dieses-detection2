from dataclasses import dataclass
from pathlib import Path
import os
from objectDetection.config.configuration import configurationManager
import keras.src.saving
import keras
from objectDetection.constants import *
from objectDetection.utils.common import read_yamal, create_directories

"""entity"""
@dataclass
class TrainingConfig:
    root_dir: Path
    training_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    params_epoch: int
    params_batch_size: int
    params_is_augmentation: bool
    params_image_size: list

@dataclass(frozen=True)
class PrepareCallbacksConfig:
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path

"""config"""
class ConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):

                 self.config = read_yamal(config_filepath)
                 self.params = read_yamal(params_filepath)
                 create_directories([self.config.artifacts_root])

    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return prepare_callback_config


    def get_training_config(self) -> TrainingConfig:

        training = self.config.training
        prepare_base_model_path = self.config.prepare_base_model
        params =self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir,'training')
        create_directories([Path(training.root_dir)])


        training_config = TrainingConfig(
            root_dir= Path(training.root_dir),
            training_model_path= Path(training.training_model_path),
            updated_base_model_path= Path(prepare_base_model_path.updated_base_model_path),
            training_data= Path(training_data),
            params_epoch= params.EPOCHS,
            params_batch_size = params.BATCH_SIZE,
            params_is_augmentation = params.AUGMENTATION,
            params_image_size = params.IMAGE_SIZE
        )


        return training_config




""" components"""


class PrepareCallback:
    def __init__(self, config:PrepareCallbacksConfig):
        self.config = config


    @property
    def _create_tb_callbacks(self):
        timestamp =time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(self.config.tensorboard_root_log_dir, f"tb_log_at_{timestamp}")

        return callbacks.TensorBoard(log_dir = tb_running_log_dir)



    @property
    def  _create_ckpt_callbacks(self):
        return callbacks.ModelCheckpoint(
            filepath=self.config.checkpoint_model_filepath,
            save_best_only=True)



    def get_tb_callbacks(self):
        return[
            self._create_tb_callbacks,
            self._create_ckpt_callbacks
        ]




# try:
#     config = configurationManager()
#     prepare_callbacks_config = config.get_prepare_callback_config()
#     prepare_callbacks = PrepareCallback(config =prepare_callbacks_config)
#     callback_list = prepare_callbacks.get_tb_callbacks()
#
# except Exception as e:
#     raise  e



"""training components"""
from objectDetection.constants import *
import os
import urllib.request as request
from zipfile import ZipFile
import  tensorflow as tf
import  time
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator
from keras._tf_keras.keras import callbacks
class Training:
    def __init__(self, config:TrainingConfig):
        self.config = config

    def get_base_model(self):
        #self.model =  tf.keras.models.load_model
        self.model = keras.saving.load_model( filepath=self.config.updated_base_model_path)


    def train_valid_generator(self):

        datagenerator_kwarg = dict(
            rescale = 1./255,
            validation_split = 0.20
        )

        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size= self.config.params_batch_size,
            interpolation ="billinear"
        )

        valid_datagenerator = ImageDataGenerator(**datagenerator_kwarg)

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset = "validation",
            shuffle=False,
            **dataflow_kwargs
        )


        if self.config.params_is_augmentation:
            train_datagenerator = ImageDataGenerator(
                rotation_range= 40,
                horizontal_flip= True,
                width_shift_range= 0.2,
                height_shift_range= 0.2,
                shear_range= 0.2,
                zoom_range= 0.2,
                **datagenerator_kwarg)
        else:
            train_datagenerator = valid_datagenerator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset =Training,
            shuffle=True,
            **dataflow_kwargs
        )
    @staticmethod
    def save_model(path: Path, model: keras.Model):
        model.save(path)

    def train(self,callback_list: list):
        self.step_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        self.model.fit(
            self.train_generator,
            epoch =self.config.params_epoch,
            step_per_epoch = self.step_per_epoch,
            validation_steps = self.validation_steps,
            validation_data = self.valid_generator,
            callback = callback_list
        )

        self.save_model(
            path = self.config.training_model_path,
            model = self.model
        )


try:
    config = ConfigurationManager()
    prepare_callbacks_config  = config.get_prepare_callback_config()
    prepare_callbacks = PrepareCallback(config =prepare_callbacks_config)
    callback_list = prepare_callbacks.get_tb_callbacks()

    training_config = config.get_training_config()
    training = Training(config = training_config)
    training.get_base_model()
    training.train_valid_generator()
    training.train(callback_list=callback_list)
except Exception as e:
    raise  e
