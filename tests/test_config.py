import importlib
import os
import pytest


def test_missing_storage_path(monkeypatch):
    monkeypatch.delenv("STORAGE_PATH", raising=False)
    monkeypatch.setenv("OUTPUT_FORMAT", "json")
    with pytest.raises(RuntimeError):
        importlib.reload(importlib.import_module("workweek_survey.config")).get_settings()


def test_settings_loaded(monkeypatch, tmp_path):
    monkeypatch.setenv("STORAGE_PATH", str(tmp_path))
    monkeypatch.setenv("OUTPUT_FORMAT", "yaml")
    mod = importlib.reload(importlib.import_module("workweek_survey.config"))
    settings = mod.get_settings()
    assert settings.storage_path == str(tmp_path)
    assert settings.output_format == "yaml"
