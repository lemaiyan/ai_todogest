#!/usr/bin/env bash
celery -A configurations  worker -c 2 --without-mingle --without-heartbeat --loglevel=info -Q celery,chatgpt_fetch_content,calendar_add_to_calendar