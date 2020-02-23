from django.apps import AppConfig
import os

default_app_config = 'file.FileConfig'

# VERBOSE_APP_NAME = u"1-家谱中心"

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class FileConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "2.1-谱书内容中心"

