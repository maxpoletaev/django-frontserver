from frontserver.settings import BUILDER_COMMAND, BUILDER_ARGS
from frontserver.utils import ExitHooks
from django.conf import settings
import os, atexit
import subprocess

from django.core.management.commands.runserver import \
    BaseRunserverCommand

PROJECT_NAME = settings.ROOT_URLCONF.split('.')[0]
LOCKFILE = '/tmp/gulpserver_%s.pid' % PROJECT_NAME
hooks = ExitHooks()
hooks.hook()


class Command(BaseRunserverCommand):
    help = 'Run static server with gulp'

    def add_arguments(self, parser):
        parser.add_argument('--gulp-app', dest='gulp_app', default=None,
            help='Run gulp only for this app.')
        super().add_arguments(parser)

    def inner_run(self, *args, **options):
        atexit.register(self.unlock_pid)

        if not self.is_running():
            self.start_gulp(app=options['gulp_app'])
            self.lock_pid()

        super().inner_run(*args, **options)

    def lock_pid(self):
        open(LOCKFILE, 'a').close()
        self.stdout.write('Gulp started')

    def unlock_pid(self):
        if hooks.exit_code == None:
            if self.is_running():
                self.stdout.write('Gulp stopped')
                os.remove(LOCKFILE)

    def is_running(self):
        return os.path.isfile(LOCKFILE)

    def start_gulp(self, app=None):
        proc_args = dict(shell=True, stdin=subprocess.PIPE,
            stdout=self.stdout, stderr=self.stderr)

        task = app if app else 'default'
        command = ' '.join([BUILDER_COMMAND, task, BUILDER_ARGS])
        subprocess.Popen([command], **proc_args)

        task = app + ':watch' if app else 'watch'
        command = ' '.join([BUILDER_COMMAND, task, BUILDER_ARGS])
        subprocess.Popen([command], **proc_args)
