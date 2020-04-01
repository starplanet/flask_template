# -*- coding: utf-8 -*-
import logging

LOG_PATH = '/data/logs/proj'
PID_FILE = 'proj.pid'

bind = '%s:%s' % ('0.0.0.0', 80)
workers = 4
worker_connections = 100
preload_app = True
timeout = 600
deamon = False
debug = False
loglevel = 'info'
pidfile = '%s/%s' % (LOG_PATH, PID_FILE)

accesslog = '-'

