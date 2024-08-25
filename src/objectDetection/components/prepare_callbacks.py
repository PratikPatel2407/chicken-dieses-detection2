from objectDetection.entity.config_entity import PrepareCallbacksConfig
import os
import time
from keras._tf_keras.keras import callbacks
from objectDetection.config.configuration import configurationManager


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




try:
    config = configurationManager()
    prepare_callbacks_config = config.get_prepare_callback_config()
    prepare_callbacks = PrepareCallback(config =prepare_callbacks_config)
    callback_list = prepare_callbacks.get_tb_callbacks()

except Exception as e:
    raise  e