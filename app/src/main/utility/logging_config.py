# # import logging

# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',style=)
# # logger = logging.getLogger(__name__)

# import logging
# import colorlog

# handler = colorlog.StreamHandler()
# handler.setFormatter(colorlog.ColoredFormatter(
#     '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
#     log_colors={
#         'DEBUG':    'cyan',
#         'INFO':     'green',
#         'WARNING':  'yellow',
#         'ERROR':    'red',
#         'CRITICAL': 'red,bg_white',
#     }
# ))

# logger = colorlog.getLogger(__name__)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# # logger.info("This is green!")
# # logger.error("This is red!")


import logging
import colorlog

handler = colorlog.StreamHandler()


handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s%(reset)s - %(message)s',
    log_colors={
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

