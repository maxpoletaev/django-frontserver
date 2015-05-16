# Django frontserver

Run grunt/gulp watcher and django server with a single command.

## Install

```
pip install django-frontserver
```

## Usage

Add `frontserver` to `INSTALLED_APPS` and run:

```sh
$ python manage.py frontserver [--app=app_name] [runserver-args]
```

This is the same as:

```sh
$ python manage.py runserver
$ gulp default
$ gulp watch
```

Or this if `--app=blog`:

```sh
$ python manage.py runserver
$ gulp blog:watch
$ gulp blog
```

## Configuration

```py
FRONTSERVER = {
    'BUILDER': 'gulp', # Command for run
    'BUILDER_ARGS': '', # Additional command-line arguments
    'DEFAULT_TASK': 'default', # Name of default task
    'WATCH_TASK': 'watch', # Name of watch task
}
```
