import requests
from git import GitCommandError

from mct import git_ops


def test_server_reachable_true_on_2xx(monkeypatch) -> None:
    class FakeResponse:
        status_code = 200

    monkeypatch.setattr(git_ops.requests, "get", lambda url, timeout: FakeResponse())
    assert git_ops.server_reachable("https://example.com") is True


def test_server_reachable_false_on_5xx(monkeypatch) -> None:
    class FakeResponse:
        status_code = 503

    monkeypatch.setattr(git_ops.requests, "get", lambda url, timeout: FakeResponse())
    assert git_ops.server_reachable("https://example.com") is False


def test_server_reachable_false_on_exception(monkeypatch) -> None:
    def raise_exc(url, timeout):
        raise requests.RequestException("boom")

    monkeypatch.setattr(git_ops.requests, "get", raise_exc)
    assert git_ops.server_reachable("https://example.com") is False


def test_remote_repo_exists_true(monkeypatch) -> None:
    class FakeGit:
        def ls_remote(self, url):
            return "deadbeef\tHEAD\n"

    monkeypatch.setattr(git_ops, "Git", FakeGit)
    assert git_ops.remote_repo_exists("https://example.com/u/r.git") is True


def test_remote_repo_exists_false_on_error(monkeypatch) -> None:
    class FakeGit:
        def ls_remote(self, url):
            raise GitCommandError("ls-remote", 128)

    monkeypatch.setattr(git_ops, "Git", FakeGit)
    assert git_ops.remote_repo_exists("https://example.com/u/missing.git") is False
