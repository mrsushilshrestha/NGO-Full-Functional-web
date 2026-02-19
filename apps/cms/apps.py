from django.apps import AppConfig


class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cms'
    verbose_name = 'Custom CMS'

    def ready(self):
        import apps.cms.signals  # noqa: F401
