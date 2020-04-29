{"filter":false,"title":"log.py","tooltip":"/market_maker/utils/log.py","undoManager":{"mark":9,"position":9,"stack":[[{"start":{"row":0,"column":0},"end":{"row":13,"column":17},"action":"insert","lines":["import logging","from market_maker import settings","","","def setup_custom_logger(name, log_level=settings.LOG_LEVEL):","    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')","","    handler = logging.StreamHandler()","    handler.setFormatter(formatter)","","    logger = logging.getLogger(name)","    logger.setLevel(log_level)","    logger.addHandler(handler)","    return logger"],"id":1}],[{"start":{"row":13,"column":17},"end":{"row":14,"column":0},"action":"insert","lines":["",""],"id":2},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"remove","lines":["    "],"id":3}],[{"start":{"row":13,"column":17},"end":{"row":14,"column":0},"action":"remove","lines":["",""],"id":4}],[{"start":{"row":13,"column":17},"end":{"row":14,"column":0},"action":"insert","lines":["",""],"id":5},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"remove","lines":["    "],"id":6}],[{"start":{"row":13,"column":17},"end":{"row":14,"column":0},"action":"insert","lines":["",""],"id":7},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"remove","lines":["    "],"id":8},{"start":{"row":13,"column":17},"end":{"row":14,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":13,"column":17},"end":{"row":14,"column":0},"action":"insert","lines":["",""],"id":9},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"remove","lines":["    "],"id":10}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":20,"selection":{"start":{"row":14,"column":0},"end":{"row":14,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":31,"mode":"ace/mode/python"}},"timestamp":1586697495617,"hash":"e408e6cb1055b911c7c5cff0569d96669302ede5"}