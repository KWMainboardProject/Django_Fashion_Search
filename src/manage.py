#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# set path
import sys
from pathlib import Path
import os

FILE = Path(__file__).resolve()
ROOT = FILE.parent
DETECT_DIR = ROOT / "analysis"
print(DETECT_DIR)
tmp = DETECT_DIR
if str(tmp) not in sys.path and os.path.isabs(tmp):
    sys.path.append(str(tmp))  # add ROOT to PATH


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fashion_api.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
