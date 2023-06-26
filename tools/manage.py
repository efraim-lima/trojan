#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# # Defina o DJANGO_SETTINGS_MODULE antes de importar qualquer coisa do Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# # Certifique-se de que o diretório do projeto esteja no sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# # Importe as configurações do Django
# import django
# django.setup()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
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
