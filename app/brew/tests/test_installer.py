from unittest.mock import patch

from brew.installer import is_homebrew_installed, install_homebrew, disable_analytics


class TestInstaller:
    @patch("brew.installer.shutil.which", return_value="/opt/homebrew/bin/brew")
    def test_is_homebrew_installed_true(self, _mock):
        assert is_homebrew_installed() is True

    @patch("brew.installer.shutil.which", return_value=None)
    def test_is_homebrew_installed_false(self, _mock):
        assert is_homebrew_installed() is False

    @patch("brew.installer.shutil.which", return_value="/opt/homebrew/bin/brew")
    def test_install_homebrew_skips_when_installed(self, _mock):
        install_homebrew(dry_run=True)

    def test_disable_analytics_dry_run(self):
        disable_analytics(dry_run=True)
