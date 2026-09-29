"""parser 单元测试。"""
import pytest

from git_tidy.parser import parse, validate


def test_parse_valid_header():
    parsed = parse("feat(core): add monthly rollup")
    assert parsed.type == "feat"
    assert parsed.scope == "core"
    assert parsed.subject == "add monthly rollup"


def test_parse_with_breaking_change():
    parsed = parse("feat!: drop python 3.8 support\n\nBREAKING CHANGE: 3.8 EOL")
    assert parsed.breaking is True


def test_parse_invalid_header_raises():
    with pytest.raises(ValueError):
        parse("not a conventional commit")


def test_validate_rejects_unknown_type():
    vs = validate("foo: whatever", ["feat", "fix"])
    codes = [v.code for v in vs]
    assert "E002" in codes


def test_validate_rejects_long_line():
    vs = validate("fix: " + "x" * 100, ["feat", "fix"], max_line_length=72)
    assert any(v.code == "E004" for v in vs)


def test_validate_passes_clean_message():
    vs = validate("fix(ui): correct button offset", ["feat", "fix", "ui"])
    assert vs == []


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
