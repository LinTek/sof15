#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sof15.settings")
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("SECRET_KEY", "dev-unsafe")
    os.environ.setdefault("DATABASE_URL", "sqlite:///db.sqlite3")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)