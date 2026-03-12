import plistlib
from unittest.mock import patch

import pytest

from updater.scheduler import (
    _build_plist,
    schedule_updates,
    unschedule_updates,
    get_schedule_status,
    LABEL,
    _INTERVAL_PRESETS,
)


class TestBuildPlist:
    def test_structure(self, tmp_path):
        log_dir = tmp_path / "logs"
        plist = _build_plist(86400, "/usr/local/bin/dev-bootstrap", log_dir)
        assert plist["Label"] == LABEL
        assert plist["StartInterval"] == 86400
        assert plist["ProgramArguments"] == ["/usr/local/bin/dev-bootstrap", "update"]
        assert plist["RunAtLoad"] is False
        assert log_dir.exists()

    def test_creates_log_dir(self, tmp_path):
        log_dir = tmp_path / "nested" / "logs"
        _build_plist(3600, "/bin/test", log_dir)
        assert log_dir.exists()


class TestScheduleUpdates:
    @patch("updater.scheduler._find_dev_bootstrap", return_value="/usr/local/bin/dev-bootstrap")
    def test_dry_run(self, _mock):
        info = schedule_updates("daily", dry_run=True)
        assert info.installed is False
        assert info.interval_seconds == 86400
        assert info.label == LABEL

    @patch("updater.scheduler._find_dev_bootstrap", return_value=None)
    def test_raises_when_no_executable(self, _mock):
        with pytest.raises(RuntimeError, match="Cannot find"):
            schedule_updates("daily")

    def test_invalid_interval(self):
        with pytest.raises(ValueError, match="Unknown interval"):
            schedule_updates("biweekly")


class TestUnscheduleUpdates:
    def test_no_existing_schedule(self):
        assert unschedule_updates(dry_run=True) is False

    @patch("updater.scheduler.PLIST_PATH")
    def test_existing_schedule_dry_run(self, mock_path):
        mock_path.exists.return_value = True
        assert unschedule_updates(dry_run=True) is True


class TestGetScheduleStatus:
    def test_not_installed(self):
        info = get_schedule_status()
        assert info.label == LABEL

    def test_installed(self, tmp_path):
        plist_file = tmp_path / "test.plist"
        data = {
            "Label": LABEL,
            "ProgramArguments": ["/usr/local/bin/dev-bootstrap", "update"],
            "StartInterval": 604800,
        }
        with open(plist_file, "wb") as f:
            plistlib.dump(data, f)

        with patch("updater.scheduler.PLIST_PATH", plist_file):
            info = get_schedule_status()
            assert info.installed is True
            assert info.interval_seconds == 604800


class TestIntervalPresets:
    def test_hourly(self):
        assert _INTERVAL_PRESETS["hourly"] == 3600

    def test_daily(self):
        assert _INTERVAL_PRESETS["daily"] == 86400

    def test_weekly(self):
        assert _INTERVAL_PRESETS["weekly"] == 604800
