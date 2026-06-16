import argparse
from pathlib import Path

from mct import config
from mct.commands import set as set_cmd


def test_set_default_updates_existing_template(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a", "b"], "default_template": "a"})

    set_cmd.run_default(argparse.Namespace(template_name="b"))

    data = config.load(rc_path)
    assert data["default_template"] == "b"


def test_set_default_rejects_unknown_template(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a"]})

    try:
        set_cmd.run_default(argparse.Namespace(template_name="missing"))
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1

    data = config.load(rc_path)
    assert "default_template" not in data
    assert data["templates"] == ["a"]
