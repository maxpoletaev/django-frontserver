from setuptools import setup, find_packages

setup(
    name='django-frontserver',
    version='0.3.3',
    packages=find_packages(),
    author='Maxim Poletaev',
    author_email='zenwalker2@gmail.com',
    url='https://github.com/zenwalker/django-frontserver',
    description='Run grunt/gulp watcher and django server with a single command.',
    keywords=['django', 'gulp', 'grunt', 'frontend'],
    classifiers=[]
)
