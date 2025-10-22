
# Music Note Recognition Game

This is a small interactive music-learning game written in Python with pygame.
Players identify notes on the staff for Treble and Bass clefs.

## Main Interface Screenshot

![Main Interface](screenshot.png)

## How to Play

1. After launching, the main interface displays Treble and Bass clef images. Hovering with the mouse highlights the buttons.
2. Click either clef image to enter the corresponding practice mode:
   - Treble clef mode: Identify notes on the staff.
   - Bass clef mode: Identify notes in the bass clef.
3. Press number keys 1-7 to answer (C=1, D=2, E=3, F=4, G=5, A=6, B=7). The interface gives instant feedback (“Correct!” or “Wrong!”) and updates your score.
4. Press ESC to return to the main menu.

## How to Run

1. Install dependencies (recommended in a virtual environment):
   ```powershell
   python -m pip install -r requirements.txt
   ```
2. Make sure the `assets/` folder contains `g-clef.png` and `f-clef.png`.
3. Run:
   ```powershell
   python music_note_game.py
   ```

## Packaging as Windows .exe (PyInstaller)

1. Install PyInstaller:
   ```powershell
   python -m pip install pyinstaller
   ```
2. Generate a single executable file (in the project root):
   ```powershell
   pyinstaller --onefile --windowed --add-data "assets;assets" music_note_game.py
   ```
   - `--add-data "assets;assets"` includes the local assets folder in the package.
   - The generated exe will be in the `dist\` folder.

## Packaging for Mac and Android

- Mac: Use PyInstaller or py2app on a Mac to package.
- Android: It is recommended to rewrite the interface with Kivy and package using Buildozer.

## Project Structure

- `music_note_game.py` - Main program
- `assets/` - Clef image resources
- `requirements.txt` - Dependencies
- `README.md` - Documentation

## License

You may choose your own open source license (this template does not include a license file).
