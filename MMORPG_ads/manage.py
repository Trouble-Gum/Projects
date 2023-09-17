#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import dotenv

import project.settings
from dotenv import load_dotenv

env = os.environ.get
DOTENV_PATH = '.env/config.env'


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':

    if os.path.exists(DOTENV_PATH):
        load_dotenv(DOTENV_PATH, override=True)
    conf = dict(dotenv.dotenv_values(DOTENV_PATH))
    mod = sys.modules['project.settings']
    list(map(lambda x: setattr(mod,
                               x[0],
                               int(x[1]) if x[1].isdigit()
                               else True if x[1] == 'True'
                               else False if x[1] == 'False'
                               else x[1]
                               ),
             conf.items()))
    main()
