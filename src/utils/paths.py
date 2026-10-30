import sys
import os


def resource_path(rel: str) -> str:
    """Absolute path to a read-only bundled resource (images, fonts, models)."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(base, rel)


def app_dir() -> str:
    """Directory next to the .exe (writable: logs, captures, serial_id)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
