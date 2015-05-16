from frontserver.utils import ExitHooks
from django.conf import settings
import os, atexit
import subprocess

from frontserver.settings import BUILDER, BUILDER_ARGS, \
    DEFAULT_TASK, WATCH_TASK

from django.core.management.commands.runserver import \
    BaseRunserverCommand

PROJECT_NAME = settings.ROOT_URLCONF.split('.')[0]
LOCKFILE = '/tmp/frontserver_%s.lock' % PROJECT_NAME

hooks = ExitHooks()
hooks.hook()


class Command(BaseRunserverCommand):
    help = 'Run static server with your frontend task runner'

    def add_arguments(self, parser):
        parser.add_argument('--app', dest='app', default=None,
            help='Run watch only for this app.')
        super().add_arguments(parser)

    def inner_run(self, *args, **options):
        atexit.register(self.unlock_pid)

        if not self.is_running():
            self.run_builder(app=options['app'])
            self.lock_pid()

        super().inner_run(*args, **options)

    def lock_pid(self):
        open(LOCKFILE, 'a').close()

    def unlock_pid(self):
        if hooks.exit_code == None:
            if self.is_running():
                os.remove(LOCKFILE)

    def is_running(self):
        return os.path.isfile(LOCKFILE)

    def run_builder(self, app=None):
        proc_args = dict(shell=True, stdin=subprocess.PIPE,
            stdout=self.stdout, stderr=self.stderr)

        task = app if app else DEFAULT_TASK
        command = ' '.join([BUILDER, task, BUILDER_ARGS])
        subprocess.Popen([command], **proc_args)

        task = app + ':' + WATCH_TASK if app else WATCH_TASK
        command = ' '.join([BUILDER, task, BUILDER_ARGS])
        subprocess.Popen([command], **proc_args)
