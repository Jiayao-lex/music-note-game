
# Music Note Recognition Game

This is a small interactive music-learning game written in Python with pygame.
Players identify notes on the staff for Treble and Bass clefs with visual and audio feedback.

## Features

- 🎼 **Dual Clef Support**: Practice both Treble and Bass clef note recognition
- 🎵 **Audio Playback**: Hear the correct pitch after answering (using generated sine wave tones)
- 🎆 **Fireworks Animation**: Celebration animation every 10 points
- 📊 **Score Tracking**: Real-time score display and feedback
- 🎹 **Interactive Learning**: Press SPACE to hear the current note, answer with 1-7 keys

## Main Interface Screenshot

![Main Interface](screenshot.png)

## How to Play

1. After launching, the main interface displays Treble and Bass clef images. Hovering with the mouse highlights the buttons.
2. Click either clef image to enter the corresponding practice mode:
   - **Treble clef mode**: Identify notes on the treble staff (C4-A5).
   - **Bass clef mode**: Identify notes on the bass staff (E2-C4).
3. **Controls**:
   - Press **1-7** to answer (C=1, D=2, E=3, F=4, G=5, A=6, B=7)
   - Press **SPACE** to hear the current note's pitch
   - Press **ESC** to return to the main menu
4. After answering:
   - **Correct**: Hear the note and gain 1 point
   - **Wrong**: Hear the correct note to learn from your mistake
5. **Every 10 points**: Enjoy a colorful fireworks celebration! 🎆

## How to Run

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```powershell
   git clone https://github.com/Jiayao-lex/music-note-game.git
   cd music-note-game
   ```

2. Install dependencies (recommended in a virtual environment):
   ```powershell
   python -m pip install -r requirements.txt
   ```
   Dependencies include:
   - `pygame>=2.0` - Game engine and graphics
   - `numpy>=1.20.0` - Audio generation for note pitches

3. Make sure the `assets/` folder contains `g-clef.png` and `f-clef.png`.

4. Run the game:
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

- `music_note_game.py` - Main program with game logic
- `assets/` - Clef image resources (g-clef.png, f-clef.png)
- `requirements.txt` - Python dependencies (pygame, numpy)
- `README.md` - Documentation
- `music_note_game.spec` - PyInstaller configuration

## Technical Details

### Audio System
- Uses **numpy** to generate accurate sine wave tones for each note
- Frequencies based on A4 = 440Hz standard tuning
- Envelope (fade in/out) to prevent audio popping
- Supports notes from E2 (82.41Hz) to A5 (880Hz)

### Visual Effects
- **Particle System**: 50 particles per firework with gravity simulation
- **Color Variety**: 6 different firework colors
- **Smooth Animation**: 60 FPS gameplay

### Note Recognition
- **Treble Clef**: 13 notes (C4 to A5)
- **Bass Clef**: 13 notes (E2 to C4)
- Accurate staff line positioning with ledger lines for out-of-range notes

## License

You may choose your own open source license (this template does not include a license file).
