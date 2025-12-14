import logging

from ai.utils.logger import get_logger


def test_get_logger_sets_level():
    logger = get_logger("test-logger-level", level=logging.DEBUG)
    assert logger.level == logging.DEBUG


def test_get_logger_adds_single_handler():
    logger_name = "test-logger-handlers"

    logger1 = get_logger(logger_name)
    handlers_count_1 = len(logger1.handlers)

    logger2 = get_logger(logger_name)
    handlers_count_2 = len(logger2.handlers)

    assert logger1 is logger2
    assert handlers_count_1 >= 1
    assert handlers_count_2 == handlers_count_1
