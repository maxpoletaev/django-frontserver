# Django frontserver

## Usage

Add `frontserver` to `INSTALLED_APPS` and run:

```sh
python manage.py frontserver [--app=app_name]
```

This is the same as:

```sh
python manage.py runserver
gulp default
gulp watch
```

Or this if `--app=blog`:

```sh
python manage.py runserver
gulp blog:watch
gulp blog
```

## Configuration

```py
FRONTSERVER = {
    'BUILDER_COMMAND': 'gulp', # Command for run
    'BUILDER_ARGS': '', # Additional command-line arguments
}
```
