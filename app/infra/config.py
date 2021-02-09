import configparser
import os

from injector import inject


class Config:
    @inject
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._config = config

    @property
    def argo_url(self) -> str:
        return self._get_config_value('ARGO_URL', 'argo', 'url')

    @property
    def argo_username(self) -> str:
        return self._get_config_value('ARGO_USERNAME', 'argo', 'username')

    @property
    def argo_password(self) -> str:
        return self._get_config_value('ARGO_PASSWORD', 'argo', 'password')

    def _get_config_value(
            self, environemnt_variable_name: str, config_name: str, config_attribute: str,
    ) -> str:
        return (
                os.getenv(environemnt_variable_name)
                or self._config.get(config_name, config_attribute)
        )
