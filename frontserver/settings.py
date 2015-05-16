from django.conf import settings

setting_overrides = getattr(settings, 'FRONTSERVER', {})


BUILDER = setting_overrides.get('BUILDER', 'gulp')
BUILDER_ARGS = setting_overrides.get('BUILDER_ARGS', '')
WATCH_TASK = setting_overrides.get('WATCH_TASK', 'watch')
DEFAULT_TASK = setting_overrides.get('DEFAULT_TASK', 'default')
