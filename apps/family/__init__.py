from django.apps import AppConfig
import os

default_app_config = 'family.FamilyConfig'

# VERBOSE_APP_NAME = u"1-家谱中心"

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class FamilyConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "2-家谱中心"

