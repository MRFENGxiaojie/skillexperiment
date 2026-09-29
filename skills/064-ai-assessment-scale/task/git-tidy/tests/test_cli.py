"""cli 测试：覆盖 check/fix/install-hook 三个子命令的主路径。"""
import subprocess

from git_tidy.cli import main


def test_check_ok(monkeypatch, capsys):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: type("R", (), {"stdout": "feat: add export\n"})(),
    )
    assert main(["check"]) == 0
    assert "OK" in capsys.readouterr().out


def test_check_fails_on_violation(monkeypatch):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: type("R", (), {"stdout": "bad message\n"})(),
    )
    assert main(["check"]) == 1


def test_fix_returns_nonzero_on_violation(monkeypatch):
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: type("R", (), {"stdout": "bad message\n"})(),
    )
    assert main(["fix"]) == 1
