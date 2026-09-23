"""Build deterministic skill ZIPs from checked-out, commit-pinned sources."""
import json
from pathlib import Path
import re
import zipfile

EXCLUDED = {'.git', '__pycache__', '.venv', 'dist', '.DS_Store'}


def build_skill(source: Path, name: str, output: Path, license_path: Path) -> Path:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Invalid skill name')
    if not (source / 'SKILL.md').is_file():
        raise ValueError(f'{name}: missing SKILL.md; initialize submodules with git submodule update --init --recursive')
    members = {}
    for path in sorted(source.rglob('*')):
        rel = path.relative_to(source)
        if any(p in EXCLUDED or p.startswith('.') for p in rel.parts):
            continue
        if rel.parts[:2] == ('docs', 'archive'):
            continue
        if path.is_symlink():
            raise ValueError(f'Unexpected symbolic link: {rel}')
        if path.is_file():
            members[f'{name}/{rel.as_posix()}'] = path.read_bytes()
    if f'{name}/LICENSE' not in members:
        members[f'{name}/LICENSE'] = license_path.read_bytes()
    output.mkdir(parents=True, exist_ok=True)
    target = output / f'{name}.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for member, data in sorted(members.items()):
            info = zipfile.ZipInfo(member, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return target


def main():
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / 'bundle.json').read_text())
    for name, path in config['skills'].items():
        source = (root / path).resolve()
        if not source.is_relative_to(root):
            raise ValueError('Skill source must remain inside this checkout')
        print(build_skill(source, name, root / 'dist', root / 'LICENSE'))


if __name__ == '__main__':
    main()
