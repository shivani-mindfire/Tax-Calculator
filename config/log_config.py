from logging import *
from datetime import datetime, timezone

basicConfig(filename = 'app.log',level=DEBUG,filemode='w',
            format="{message}|{asctime}:{lineno}:{process}:{levelname}:{name}",
            style="{")

logger = getLogger()
# debug("This is a debug message")
# info("All the inputs are correct")
# warning("The warning message is displaying")
# error("The error message is displaying")
# critical("The critical message is displaying")