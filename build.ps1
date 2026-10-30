# build.ps1 - Gera dist/ALMA/ALMA.exe com PyInstaller (onedir, console)
# Execute: .\build.ps1

$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot"

pyinstaller `
    --onedir `
    --name ALMA `
    --console `
    --contents-directory . `
    --collect-all mediapipe `
    --collect-data pygame_gui `
    --collect-data face_recognition_models `
    --add-data "images;images" `
    --add-data "models;models" `
    --add-data "src\fonts;src\fonts" `
    --add-data "src\styles;src\styles" `
    --exclude-module torch `
    --exclude-module torchaudio `
    --exclude-module torchvision `
    --exclude-module faster_whisper `
    --exclude-module whisper `
    --exclude-module openai `
    --exclude-module pocketsphinx `
    --exclude-module sounddevice `
    --exclude-module edge_tts `
    --exclude-module jellyfin_mpv_shim `
    --exclude-module pyttsx3 `
    --exclude-module jax `
    --exclude-module jaxlib `
    --exclude-module tensorflow `
    --exclude-module pytest `
    main.py

Write-Host "=== Build concluido. Verifique dist\ALMA\ALMA.exe ==="
