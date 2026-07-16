from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    assert "%LOCALAPPDATA%\\ruslan\\ruslan-agent\\venv\\Scripts" in doc
    assert "Get-Command ruslan        # should print C:\\Users\\<you>\\AppData\\Local\\ruslan\\ruslan-agent\\venv\\Scripts\\ruslan.exe" in doc
    assert '$ruslanBin = "$InstallDir\\venv\\Scripts"' in install
