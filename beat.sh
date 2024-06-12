#!/usr/bin/env bash
celery -A configurations  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler