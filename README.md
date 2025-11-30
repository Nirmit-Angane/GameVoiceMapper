# 🎮 GameVoiceMapper

<div align="center">

**🎤 Control your games with your voice! 🎮**

*A powerful voice-controlled keyboard mapper for gaming, accessibility, and hands-free control*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 **Offline Voice Recognition** | Uses Vosk for instant, local processing - no internet required! |
| ⚡ **Lightning Fast** | Optimized for minimal latency with interruptible commands |
| 🎮 **Gaming Optimized** | DirectInput key simulation works with most games |
| 🔄 **Repeated Commands** | Say "left left left" to execute a command multiple times |
| ⏱️ **Duration Control** | Hold keys for specific durations (e.g., `w:5` holds W for 5 seconds) |
| 🛡️ **Interruptible** | New commands instantly cancel running ones |
| 🎨 **Modern UI** | Clean, dark-themed interface built with CustomTkinter |



## 📋 Requirements

- 🐍 **Python 3.8+**
- 💻 **Windows OS** (uses Windows-specific DirectInput API)
- 🎙️ **Microphone** with proper permissions enabled



## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/GameVoiceMapper.git
cd GameVoiceMapper
```

### 2️⃣ Install Dependencies
```bash
pip install customtkinter vosk pyaudio requests
```

### 3️⃣ Download Voice Model
Run the setup script to download the Vosk speech recognition model (~40MB):
```bash
python download_model.py
```

> 📦 This will create a `model` folder containing the offline speech recognition model.

### 4️⃣ Enable Microphone Access
> ⚠️ **Important:** Windows must allow Python to access your microphone.

1. Go to **⚙️ Settings > 🔒 Privacy > 🎙️ Microphone**
2. Enable **"Allow desktop apps to access your microphone"**
3. Ensure Python is listed and allowed ✅


## 🎯 Usage

### 🏁 Starting the Application
```bash
python main.py
```

### ➕ Adding Voice Commands

1. **🗣️ Voice Command**: The phrase you'll say (e.g., "jump")
2. **⌨️ Key Bind**: The keyboard key to press (e.g., "space")
3. **⏱️ Duration** (optional): How long to hold the key in seconds

#### 💡 Examples:
- Simple: `"jump"` → `space`
- With modifier: `"sprint"` → `shift+w`
- With duration: `"run forward"` → `w:5` (holds W for 5 seconds)

### 🎤 Voice Commands

- Say your command clearly after clicking **"START LISTENING"**
- Commands are case-insensitive
- New commands interrupt running ones instantly

## ⌨️ Supported Key Formats

| Format | Example | Description |
|--------|---------|-------------|
| **Single keys** | `w`, `space`, `enter`, `esc` | Basic key press |
| **Modifiers** | `ctrl+c`, `shift+w`, `alt+tab` | Key combinations |
| **With duration** | `w:2.5`, `space:1` | Hold for X seconds |

> 📖 See `actions.py` for the full list of supported scan codes.

## 🛠️ Troubleshooting

### 🚫 "Microphone access denied" Error
- Check Windows Privacy Settings (**Settings > Privacy > Microphone**)
- Ensure "Allow desktop apps to access your microphone" is **ON**
- 🔄 Restart the application after granting permissions

### 📁 "Model directory not found" Error
- ▶️ Run `python download_model.py` to download the voice model
- Ensure the `model` folder exists in the project directory

### ❌ Commands Not Recognized
- Speak clearly and at normal volume
- Ensure the game/application window is in focus
- Check that your command is added in the UI

### 🐌 Slow Recognition
- The app uses offline recognition (Vosk) for instant processing
- First-time model loading takes a few seconds
- Subsequent recognitions are near-instant


## 📂 Project Structure

```
GameVoiceMapper/
├── main.py              # Application entry point
├── ui.py                # CustomTkinter GUI
├── listener.py          # Vosk voice recognition logic
├── actions.py           # DirectInput key simulation
├── commands.json        # Saved voice commands
├── download_model.py    # Model download script
├── model/               # Vosk speech model (gitignored)
└── README.md            # This file
```

## ⚙️ How It Works


1. **Voice Input**: Captures audio from your microphone using PyAudio
2. **Recognition**: Processes speech locally using Vosk (offline)
3. **Command Matching**: Matches recognized text to your saved commands
4. **Key Simulation**: Simulates keypresses using Windows DirectInput API
5. **Interruption**: New commands cancel running ones for instant response


## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) - 🎤 Offline speech recognition
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - 🎨 Modern UI framework
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) - 🔊 Audio I/O

---

<div align="center">

**Made with ❤️ for gamers and accessibility**

⭐ Star this repo if you find it useful!

</div>
