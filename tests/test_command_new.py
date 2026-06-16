import argparse
from pathlib import Path

from mct import config
from mct.commands import new


def make_args(**overrides) -> argparse.Namespace:
    defaults = dict(template_site_path=None, username=None, template="tmpl", new_name="proj")
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_new_aborts_when_server_unreachable(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    config.save(tmp_path / config.MCTRC_FILENAME, {"template_site_path": "https://example.com", "username": "u", "templates": []})
    monkeypatch.setattr(new.git_ops, "server_reachable", lambda url: False)

    try:
        new.run(make_args())
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1


def test_new_aborts_when_template_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    config.save(tmp_path / config.MCTRC_FILENAME, {"template_site_path": "https://example.com", "username": "u", "templates": []})
    monkeypatch.setattr(new.git_ops, "server_reachable", lambda url: True)
    monkeypatch.setattr(new.git_ops, "remote_repo_exists", lambda url: False)

    try:
        new.run(make_args())
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1


def test_new_aborts_when_dest_exists(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    config.save(tmp_path / config.MCTRC_FILENAME, {"template_site_path": "https://example.com", "username": "u", "templates": []})
    (tmp_path / "proj").mkdir()
    monkeypatch.setattr(new.git_ops, "server_reachable", lambda url: True)
    monkeypatch.setattr(new.git_ops, "remote_repo_exists", lambda url: True)

    try:
        new.run(make_args())
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1


def test_new_clones_and_reports_existing_remote(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    config.save(tmp_path / config.MCTRC_FILENAME, {"template_site_path": "https://example.com", "username": "u", "templates": []})

    monkeypatch.setattr(new.git_ops, "server_reachable", lambda url: True)
    monkeypatch.setattr(new.git_ops, "remote_repo_exists", lambda url: True)

    class FakeRepo:
        class remotes:
            class origin:
                set_url_calls = []

                @classmethod
                def set_url(cls, url):
                    cls.set_url_calls.append(url)

    monkeypatch.setattr(new.git_ops, "clone", lambda url, dest: FakeRepo())

    new.run(make_args())

    out = capsys.readouterr().out
    assert "already exists. You can push to it now." in out
    assert FakeRepo.remotes.origin.set_url_calls == ["https://example.com/u/proj.git"]
