from django.conf import settings

setting_overrides = getattr(settings, 'FRONTSERVER', {})

BUILDER_COMMAND = setting_overrides.get('BUILDER_COMMAND', 'gulp')
BUILDER_ARGS = setting_overrides.get('BUILDER_ARGS', '')
