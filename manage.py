#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

"""
ooo        ooooo   .oo.       .oooooo.         .o.        .oooooo..o 
`88.       .888' .88' `8.    d8P'  `Y8b       .888.      d8P'    `Y8 
 888b     d'888  88.  .8'   888      888     .8"888.     Y88bo.      
 8 Y88. .P  888  `88.8P     888      888    .8' `888.     `"Y8888o.  
 8  `888'   888   d888[.8'  888      888   .88ooo8888.        `"Y88b 
 8    Y     888  88' `88.   `88b    d88'  .8'     `888.  oo     .d8P 
o8o        o888o `bodP'`88.  `Y8bood8P'  o88o     o8888o 8""88888P'  
"""


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MOAS.settings')
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
