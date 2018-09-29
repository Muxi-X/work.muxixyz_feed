#! /bin/bash
gunicorn --name work_feed --timeout "120" --log-level debug -b 0.0.0.0:1668 -w 4 wsgi:app

