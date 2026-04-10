#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Ensure the inner project package is on sys.path so the settings
    # module can be imported whether this script is run from the repo root
    # or from the inner project directory.
    base_dir = os.path.dirname(__file__)
    inner_pkg_path = os.path.join(base_dir, 'auto_alert_accident')
    if inner_pkg_path not in sys.path:
        sys.path.insert(0, inner_pkg_path)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_alert_accident.settings')
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
    main()
