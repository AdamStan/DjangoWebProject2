from django.contrib import admin
from django.apps import apps
from .apps import *

app = apps.get_app_config(EntitiesConfig.static_name)

# Register your models here.
for module_name, module in app.models.items():
    admin.site.register(module)
