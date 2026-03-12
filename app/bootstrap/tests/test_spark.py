from unittest.mock import patch, MagicMock
from pathlib import Path

from bootstrap.spark import _detect_spark_home


class TestDetectSparkHome:
    @patch("bootstrap.spark.get_brew_paths")
    @patch("bootstrap.spark.get_platform")
    def test_no_spark_installed(self, mock_plat, mock_paths):
        mock_paths.return_value = MagicMock(cellar=Path("/nonexistent/Cellar"))
        result = _detect_spark_home()
        assert result is None

    @patch("bootstrap.spark.get_brew_paths")
    @patch("bootstrap.spark.get_platform")
    def test_spark_installed(self, mock_plat, mock_paths, tmp_path):
        cellar = tmp_path / "Cellar" / "apache-spark"
        spark_dir = cellar / "3.5.0" / "libexec"
        spark_dir.mkdir(parents=True)
        mock_paths.return_value = MagicMock(cellar=tmp_path / "Cellar")

        result = _detect_spark_home()
        assert result == spark_dir

    @patch("bootstrap.spark.get_brew_paths")
    @patch("bootstrap.spark.get_platform")
    def test_picks_latest_version(self, mock_plat, mock_paths, tmp_path):
        cellar = tmp_path / "Cellar" / "apache-spark"
        (cellar / "3.3.0" / "libexec").mkdir(parents=True)
        (cellar / "3.5.0" / "libexec").mkdir(parents=True)
        mock_paths.return_value = MagicMock(cellar=tmp_path / "Cellar")

        result = _detect_spark_home()
        assert "3.5.0" in str(result)
