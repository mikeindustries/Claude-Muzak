# Claude Muzak 🎵

Elevator music for your Claude Code tasks! Automatically plays background music while Claude is working, because coding is better with a soundtrack.

## ✨ Features

- 🎵 **Automatic playback** during Claude Code sessions (via hooks)
- ⌨️ **Easy control** with ESC, Q, or Ctrl+C to stop
- 🎲 **Random music selection** from your collection
- 🖥️ **Cross-platform support** (macOS with `afplay`)
- 🎯 **Zero dependencies** beyond Python standard library

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/claude-muzak.git
cd claude-muzak
mkdir muzakfiles
```

### 2. Add Your Music
Copy your favorite background music files to the `muzakfiles/` directory:
```bash
cp ~/Music/*.mp3 muzakfiles/
cp ~/Music/*.m4a muzakfiles/
# Any audio format: MP3, M4A, WAV, AAC, FLAC, OGG
```

### 3. Test It Out
```bash
python3 claude_muzak.py start
# Press ESC, Q, or Ctrl+C to stop
```

## 📖 Usage

### Interactive Mode
```bash
python3 claude_muzak.py start    # Start music (press ESC/Q to stop)
python3 claude_muzak.py stop     # Stop music manually
```

### Run Commands with Music
Perfect for long-running tasks:
```bash
python3 claude_muzak.py run "npm test"
python3 claude_muzak.py run "make build"
python3 claude_muzak.py run "pytest"
```

### Automatic Integration with Claude Code
For automatic music during all Claude Code sessions:

1. **Find the full path** to your `claude_muzak.py`:
   ```bash
   pwd  # Copy this path
   ```

2. **Add hooks** to `~/.claude/settings.json`:
   ```json
   {
     "hooks": {
       "UserPromptSubmit": {
         "command": "python3 /full/path/to/claude_muzak.py hook start"
       },
       "SessionEnd": {
         "command": "python3 /full/path/to/claude_muzak.py hook stop"
       }
     }
   }
   ```

3. **Restart Claude Code** and enjoy automatic elevator music! 🎵

## 🎼 Supported Audio Formats

- **MP3** - Most common format
- **M4A** - iTunes/Apple Music format
- **WAV** - Uncompressed audio
- **AAC** - Advanced Audio Codec
- **FLAC** - Lossless compression
- **OGG** - Open source format

## 🔧 System Requirements

- **macOS** (uses built-in `afplay` command)
- **Python 3.6+** (no additional packages needed)
- **Audio files** in the `muzakfiles/` directory

## 🎯 Pro Tips

- **Curate your playlist**: Add calm, non-distracting background music
- **Volume control**: Use your system volume controls
- **Multiple formats**: Mix different audio formats in the same folder
- **Test first**: Run `python3 claude_muzak.py start` before setting up hooks

## 🐛 Troubleshooting

**Music won't start?**
- Check that `muzakfiles/` directory exists and contains audio files
- Verify you're on macOS (required for `afplay`)
- Try: `ls muzakfiles/` to see your audio files

**ESC key not working?**
- Try the Q key or Ctrl+C instead
- The script uses raw keyboard input for maximum compatibility

**Hook not working?**
- Double-check the full path in your settings.json
- Restart Claude Code after adding hooks
- Test the command manually first

## 📝 License

MIT License - Feel free to fork, modify, and share!

---

*Now get back to coding with your personal elevator music! 🎵*