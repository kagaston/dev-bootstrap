import logging

from logger.config import get_logger


class TestGetLogger:
    def test_returns_logger(self):
        log = get_logger("test_returns")
        assert isinstance(log, logging.Logger)
        assert log.name == "test_returns"

    def test_has_console_handler(self):
        log = get_logger("test_console")
        handler_types = [type(h) for h in log.handlers]
        assert logging.StreamHandler in handler_types

    def test_file_handler_with_log_dir(self, tmp_path):
        log = get_logger("test_file", log_dir=tmp_path)
        handler_types = [type(h) for h in log.handlers]
        assert logging.FileHandler in handler_types
        assert (tmp_path / "test_file.log").exists()

    def test_idempotent(self):
        log1 = get_logger("test_idempotent")
        log2 = get_logger("test_idempotent")
        assert log1 is log2
        assert len(log1.handlers) == 1
