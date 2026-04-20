from logging import *
from datetime import datetime, timezone

basicConfig(filename = 'app.log',level=DEBUG,filemode='w',
            format="{message}|{asctime}:{lineno}:{process}:{levelname}:{name}",
            style="{")

logger = getLogger()
