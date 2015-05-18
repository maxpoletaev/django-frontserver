from frontserver.utils import ExitHooks
from django.conf import settings
import os, atexit
import subprocess

from frontserver.settings import BUILDER, BUILDER_ARGS, \
    DEFAULT_TASK, WATCH_TASK

from django.contrib.staticfiles.management.commands.runserver import Command \
    as BaseRunserverCommand

PROJECT_NAME = settings.ROOT_URLCONF.split('.')[0]
LOCKFILE = '/tmp/frontserver_%s.lock' % PROJECT_NAME

hooks = ExitHooks()
hooks.hook()


class Command(BaseRunserverCommand):
    help = 'Run static server with your frontend task runner'

    def add_arguments(self, parser):
        parser.add_argument('--apps', dest='apps', default=None,
            help='Run watch only for this apps.')
        parser.add_argument('--nodefault', action='store_true', dest='no_default',
            default=False, help='Run server without default task.')
        parser.add_argument('--nowatch', action='store_true', dest='no_watch',
            default=False, help='Run server without watch tasks.')
        super().add_arguments(parser)

    def inner_run(self, *args, **options):
        atexit.register(self.unlock_pid)

        if not self.is_running():
            watch = not options['no_watch']
            default = not options['no_default']
            self.run_builder(apps=options['apps'], default=default, watch=watch)
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

    def run_builder(self, apps=None, default=True, watch=True):
        if apps:
            apps = apps.split(',')

        proc_args = dict(shell=True, stdin=subprocess.PIPE,
            stdout=self.stdout, stderr=self.stderr)

        tasks = []

        if default:
            if apps:
                for app in apps:
                    tasks.append(app)
            else:
                tasks.append(DEFAULT_TASK)

        if watch:
            if apps:
                for app in apps:
                    tasks.append(app + ':' + WATCH_TASK)
            else:
                tasks.append(WATCH_TASK)

        command = ' '.join([BUILDER, ' '.join(tasks), BUILDER_ARGS])
        subprocess.Popen([command], **proc_args)
