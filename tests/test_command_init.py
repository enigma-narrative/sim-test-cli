import argparse
from pathlib import Path

from mct import config
from mct.commands import init


def make_args(**overrides) -> argparse.Namespace:
    defaults = dict(template_site_path=config.DEFAULT_TEMPLATE_SITE_PATH, username="jyurkiw", templates=["a", "b"])
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_init_creates_rc_file(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init.run(make_args())

    rc_path = tmp_path / config.MCTRC_FILENAME
    data = config.load(rc_path)
    assert data == {
        "template_site_path": config.DEFAULT_TEMPLATE_SITE_PATH,
        "username": "jyurkiw",
        "templates": ["a", "b"],
        "default_template": "a",
    }


def test_init_without_templates_sets_no_default(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    init.run(make_args(templates=[]))

    rc_path = tmp_path / config.MCTRC_FILENAME
    data = config.load(rc_path)
    assert "default_template" not in data


def test_init_aborts_on_no_confirm_when_exists(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "old", "templates": []})

    monkeypatch.setattr(init.ui, "confirm", lambda message: False)
    init.run(make_args(username="new"))

    data = config.load(rc_path)
    assert data["username"] == "old"


def test_init_overwrites_on_confirm(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "old", "templates": []})

    monkeypatch.setattr(init.ui, "confirm", lambda message: True)
    init.run(make_args(username="new"))

    data = config.load(rc_path)
    assert data["username"] == "new"
