#!/bin/bash
# Claude Muzak Setup Script 🎵
# Quick setup script for Claude Muzak elevator music

set -e

echo "🎵 Setting up Claude Muzak..."
echo

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: Claude Muzak requires macOS (uses afplay command)"
    echo "   Your system: $OSTYPE"
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    echo "   Please install Python 3.6+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "✅ Found Python $PYTHON_VERSION"

# Create muzakfiles directory
if [ ! -d "muzakfiles" ]; then
    mkdir muzakfiles
    echo "✅ Created muzakfiles/ directory"
else
    echo "✅ muzakfiles/ directory already exists"
fi

# Check for audio files
AUDIO_COUNT=$(find muzakfiles -name "*.mp3" -o -name "*.m4a" -o -name "*.wav" -o -name "*.aac" -o -name "*.flac" -o -name "*.ogg" | wc -l)
if [ $AUDIO_COUNT -eq 0 ]; then
    echo "⚠️  No audio files found in muzakfiles/"
    echo "   Add some music files to get started:"
    echo "   cp ~/Music/*.mp3 muzakfiles/"
    echo "   cp ~/Music/*.m4a muzakfiles/"
else
    echo "✅ Found $AUDIO_COUNT audio files in muzakfiles/"
fi

# Test the script
echo
echo "🧪 Testing Claude Muzak..."
if python3 claude_muzak.py --help > /dev/null 2>&1; then
    echo "❌ Test failed - script doesn't run properly"
else
    echo "✅ Script runs successfully"
fi

# Show next steps
echo
echo "🎯 Setup complete! Next steps:"
echo "1. Test it: python3 claude_muzak.py start"
echo "2. Add to Claude Code hooks (see README for details)"
echo "3. Enjoy your elevator music! 🎵"
echo
echo "Full path for hooks: $(pwd)/claude_muzak.py"