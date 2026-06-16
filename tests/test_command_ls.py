import argparse
from pathlib import Path

from mct import config
from mct.commands import ls


def test_ls_renders_templates(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    rc_path = tmp_path / config.MCTRC_FILENAME
    config.save(rc_path, {"template_site_path": "x", "username": "u", "templates": ["a", "b"]})

    captured = {}
    monkeypatch.setattr(
        ls.ui, "render_table", lambda title, columns, rows: captured.update(title=title, columns=columns, rows=rows)
    )

    ls.run(argparse.Namespace())

    assert captured["columns"] == ["Template"]
    assert captured["rows"] == [("a",), ("b",)]


def test_ls_exits_without_rc(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    try:
        ls.run(argparse.Namespace())
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1
