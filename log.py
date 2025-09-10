import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
fh = logging.FileHandler(filename='example.log')
formatter = logging.Formatter("%(asctime)s %(message)s")

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


# 移除不必要的預設 logger
logger = logging.getLogger("uvicorn")
logger.handlers = []

logger_ac = logging.getLogger("uvicorn.access")
logger_ac.handlers = []