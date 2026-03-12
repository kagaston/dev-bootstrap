from unittest.mock import patch
from pathlib import Path

from settings.config import Platform, get_platform, get_brew_paths, FORMULAE, CASKS


class TestGetPlatform:
    @patch("settings.config.platform")
    def test_macos_arm(self, mock_platform):
        mock_platform.system.return_value = "Darwin"
        mock_platform.machine.return_value = "arm64"
        assert get_platform() == Platform.MACOS_ARM

    @patch("settings.config.platform")
    def test_macos_intel(self, mock_platform):
        mock_platform.system.return_value = "Darwin"
        mock_platform.machine.return_value = "x86_64"
        assert get_platform() == Platform.MACOS_INTEL

    @patch("settings.config.platform")
    def test_linux(self, mock_platform):
        mock_platform.system.return_value = "Linux"
        mock_platform.machine.return_value = "x86_64"
        assert get_platform() == Platform.LINUX

    @patch("settings.config.platform")
    def test_unsupported(self, mock_platform):
        mock_platform.system.return_value = "Windows"
        mock_platform.machine.return_value = "AMD64"
        assert get_platform() == Platform.UNSUPPORTED


class TestGetBrewPaths:
    def test_arm_paths(self):
        paths = get_brew_paths(Platform.MACOS_ARM)
        assert paths.prefix == Path("/opt/homebrew")
        assert paths.bin == Path("/opt/homebrew/bin")
        assert paths.cellar == Path("/opt/homebrew/Cellar")

    def test_intel_paths(self):
        paths = get_brew_paths(Platform.MACOS_INTEL)
        assert paths.prefix == Path("/usr/local")
        assert paths.bin == Path("/usr/local/bin")
        assert paths.cellar == Path("/usr/local/Cellar")

    def test_brew_executable(self):
        paths = get_brew_paths(Platform.MACOS_ARM)
        assert paths.brew_executable == Path("/opt/homebrew/bin/brew")


class TestPackageLists:
    def test_formulae_not_empty(self):
        assert len(FORMULAE) > 0

    def test_casks_not_empty(self):
        assert len(CASKS) > 0

    def test_git_in_formulae(self):
        assert "git" in FORMULAE
