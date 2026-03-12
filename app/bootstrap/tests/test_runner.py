from unittest.mock import patch

from bootstrap.runner import _check_platform
from settings.config import Platform


class TestCheckPlatform:
    @patch("bootstrap.runner.get_platform", return_value=Platform.MACOS_ARM)
    def test_macos_arm_supported(self, _mock):
        assert _check_platform() is True

    @patch("bootstrap.runner.get_platform", return_value=Platform.MACOS_INTEL)
    def test_macos_intel_supported(self, _mock):
        assert _check_platform() is True

    @patch("bootstrap.runner.get_platform", return_value=Platform.LINUX)
    def test_linux_unsupported(self, _mock):
        assert _check_platform() is False

    @patch("bootstrap.runner.get_platform", return_value=Platform.UNSUPPORTED)
    def test_unsupported(self, _mock):
        assert _check_platform() is False
