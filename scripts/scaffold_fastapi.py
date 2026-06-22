from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy DingTalk robot FastAPI templates into a target repo.")
    parser.add_argument("--target", required=True, help="Target repository root.")
    parser.add_argument("--package", default="app.integrations.dingtalk_robot", help="Python package path for .py templates.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = root / "assets" / "fastapi"
    target = Path(args.target).resolve()
    package_dir = target / Path(args.package.replace(".", "/"))
    docs_dir = target / "docs" / "dingtalk_robot"

    package_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    copies = [
        (source / "dingtalk_robot.py", package_dir / "dingtalk_robot.py"),
        (source / "robot_routes.py", package_dir / "robot_routes.py"),
        (source / "robot_tables.sql", docs_dir / "robot_tables.sql"),
        (source / "robot_config_example.json", docs_dir / "robot_config_example.json"),
    ]

    for src, dst in copies:
        if dst.exists() and not args.force:
            print(f"skip existing: {dst}")
            continue
        shutil.copy2(src, dst)
        print(f"copied: {dst}")

    init_file = package_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")
        print(f"created: {init_file}")


if __name__ == "__main__":
    main()
