# Minimal manage.py scaffold (not fully functional without Django installed)
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is not installed. Install Django to run the server."
        ) from exc
    execute_from_command_line(sys.argv)
