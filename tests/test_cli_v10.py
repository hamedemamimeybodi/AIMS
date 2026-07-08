from aims.cli import build_parser


def test_cli_has_release_check_command():
    parser = build_parser()
    args = parser.parse_args(["release-check", "--version", "1.0.0"])
    assert args.command == "release-check"
    assert args.version == "1.0.0"


def test_validate_default_version_is_v100():
    parser = build_parser()
    args = parser.parse_args(["validate"])
    assert args.version == "1.0.0"
