from datetime import datetime
from pathlib import Path
import cv2
import pygame

_CAPTURE_DIR = Path("Capturas")


def _next_path() -> Path:
    _CAPTURE_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return _CAPTURE_DIR / f"captura_{stamp}.png"


def save_cv2(img) -> None:
    path = _next_path()
    cv2.imwrite(str(path), img)
    print(f"[screenshot] {path}")


def save_pygame(surface: pygame.Surface) -> None:
    path = _next_path()
    pygame.image.save(surface, str(path))
    print(f"[screenshot] {path}")
