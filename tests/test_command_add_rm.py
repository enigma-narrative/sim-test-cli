import argparse
from pathlib import Path

from mct import config
from mct.commands import add, rm


def test_add_appends_new_templates_on_confirm(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a"]})

    monkeypatch.setattr(add.ui, "confirm", lambda message: True)
    monkeypatch.setattr(add.ui, "render_table", lambda *a, **k: None)

    add.run(argparse.Namespace(templates=["b", "a"]))

    data = config.load(rc_path)
    assert data["templates"] == ["a", "b"]


def test_add_aborts_without_confirm(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a"]})

    monkeypatch.setattr(add.ui, "confirm", lambda message: False)
    monkeypatch.setattr(add.ui, "render_table", lambda *a, **k: None)

    add.run(argparse.Namespace(templates=["b"]))

    data = config.load(rc_path)
    assert data["templates"] == ["a"]


def test_rm_status_classification_and_removal(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a", "b"]})

    captured = {}
    monkeypatch.setattr(
        rm.ui, "render_table", lambda title, columns, rows: captured.update(rows=rows)
    )
    monkeypatch.setattr(rm.ui, "confirm", lambda message: True)

    rm.run(argparse.Namespace(templates=["a", "c"]))

    rows_by_name = {name: status for name, status in captured["rows"]}
    assert rows_by_name == {"a": "DELETE", "b": "KEEP", "c": "NO EXIST"}

    data = config.load(rc_path)
    assert data["templates"] == ["b"]


def test_rm_aborts_without_confirm(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a", "b"]})

    monkeypatch.setattr(rm.ui, "render_table", lambda *a, **k: None)
    monkeypatch.setattr(rm.ui, "confirm", lambda message: False)

    rm.run(argparse.Namespace(templates=["a"]))

    data = config.load(rc_path)
    assert data["templates"] == ["a", "b"]
