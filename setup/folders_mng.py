#!/usr/bin/env python3

import os
from pathlib import Path

def create_folders(system, __app_name__):
    try:
        if system == 'Windows':
            base_path = Path(os.getenv("APPDATA"))
        elif system == 'Linux':
            base_path = Path.home() / ".local" / "share"
        else:
            base_path = Path.home() / ".config"

        app_path = base_path / "MJLab" / __app_name__

        if app_path.exists():
            print(f"Path already exists: {app_path}")
        else:
            app_path.mkdir(parents=True, exist_ok=True)
            print(f"Folders created: {app_path}")
        return app_path

    except Exception as e:
        print(e)