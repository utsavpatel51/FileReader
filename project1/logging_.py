import logging


def get_logger_handler():
    logFormatStr = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
    formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("app.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    return fileHandler
