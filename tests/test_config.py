from pathlib import Path

from mct import config


def test_discover_rc_in_current_dir(tmp_path: Path) -> None:
    rc = tmp_path / config.MCTRC_FILENAME
    rc.write_text('username = "u"\n')
    assert config.discover_rc(tmp_path) == rc


def test_discover_rc_in_parent_dir(tmp_path: Path) -> None:
    rc = tmp_path / config.MCTRC_FILENAME
    rc.write_text('username = "u"\n')
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)
    assert config.discover_rc(nested) == rc


def test_discover_rc_closest_wins(tmp_path: Path) -> None:
    parent_rc = tmp_path / config.MCTRC_FILENAME
    parent_rc.write_text('username = "parent"\n')
    nested = tmp_path / "child"
    nested.mkdir()
    child_rc = nested / config.MCTRC_FILENAME
    child_rc.write_text('username = "child"\n')
    assert config.discover_rc(nested) == child_rc


def test_discover_rc_not_found(tmp_path: Path) -> None:
    isolated = tmp_path / "isolated"
    isolated.mkdir()
    assert config.discover_rc(isolated) is None


def test_load_save_roundtrip(tmp_path: Path) -> None:
    rc = tmp_path / config.MCTRC_FILENAME
    data = {
        "template_site_path": "https://github.com",
        "username": "jyurkiw",
        "templates": ["a", "b"],
    }
    config.save(rc, data)
    loaded = config.load(rc)
    assert loaded == data


def test_require_rc_exits_when_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(config, "discover_rc", lambda start: None)
    try:
        config.require_rc(tmp_path)
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1
