#!/usr/bin/env python3
"""
Claude Muzak 🎵
Elevator music for Claude Code tasks

A simple background music player that integrates with Claude Code to provide
ambient music during your coding sessions. Because coding is better with a soundtrack!

Usage:
    python3 claude_muzak.py start           # Start music (press ESC/Q to stop)
    python3 claude_muzak.py stop            # Stop music manually
    python3 claude_muzak.py run <command>   # Run command with music
    python3 claude_muzak.py hook start      # Hook: start music
    python3 claude_muzak.py hook stop       # Hook: stop music

Author: Your Name
License: MIT
"""

import subprocess
import sys
import os
import signal
import random
import json
import threading
from pathlib import Path

# Try to import keyboard handling modules (Unix/macOS only)
try:
    import termios
    import tty
    import select
    KEYBOARD_AVAILABLE = True
except ImportError:
    # Windows or other platforms without termios
    KEYBOARD_AVAILABLE = False

class ClaudeMuzak:
    """
    Main class for managing elevator music playback during Claude Code tasks.

    Handles music selection, playback control, and keyboard input for stopping music.
    """

    def __init__(self):
        """Initialize the Claude Muzak player with default settings."""
        self.script_dir = Path(__file__).parent
        self.music_dir = self.script_dir / "muzakfiles"
        self.pid_file = Path("/tmp/claude_elevator_music.pid")
        self.stop_flag = threading.Event()

    def get_random_music_file(self):
        """Get a random music file from the muzakfiles directory"""
        if not self.music_dir.exists():
            raise FileNotFoundError(f"Music directory {self.music_dir} not found")

        patterns = ["*.mp3", "*.m4a", "*.wav", "*.aac", "*.flac", "*.ogg"]
        music_files = []
        for pattern in patterns:
            music_files.extend(self.music_dir.glob(pattern))

        if not music_files:
            raise FileNotFoundError(f"No audio files found in {self.music_dir}")
        return random.choice(music_files)

    def is_music_playing(self):
        """Check if music is currently playing"""
        if not self.pid_file.exists():
            return False
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False

    def start_music(self, quiet=False):
        """Start playing elevator music"""
        try:
            if self.is_music_playing():
                if not quiet:
                    print("Elevator music is already playing")
                return

            selected_music = self.get_random_music_file()
            if not quiet:
                print(f"🎵 Selected: {selected_music.name}")

            process = subprocess.Popen([
                'bash', '-c',
                f'while true; do afplay "{selected_music}"; done'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))

            if not quiet:
                print(f"🎵 Started elevator music (PID: {process.pid})")

        except Exception as e:
            if not quiet:
                print(f"Error starting music: {e}")

    def stop_music(self, quiet=False):
        """Stop playing elevator music"""
        try:
            if self.pid_file.exists():
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                try:
                    subprocess.run(['pkill', '-P', str(pid)], stderr=subprocess.DEVNULL)
                    os.kill(pid, signal.SIGTERM)
                except (OSError, subprocess.CalledProcessError):
                    pass
                self.pid_file.unlink()
                if not quiet:
                    print("🔇 Stopped elevator music")
            else:
                if not quiet:
                    print("Elevator music is not playing")

            subprocess.run(['pkill', '-f', 'afplay.*muzakfiles'], stderr=subprocess.DEVNULL)
        except Exception as e:
            if not quiet:
                print(f"Error stopping music: {e}")

    def listen_for_escape(self):
        """Listen for escape key press to stop music"""
        if not KEYBOARD_AVAILABLE:
            return
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            while not self.stop_flag.is_set():
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    try:
                        char = sys.stdin.read(1)
                        if char:
                            char_ord = ord(char)
                            # Stop on ESC, Q, or Ctrl+C
                            if char_ord in [27, 3] or char.lower() == 'q':
                                if char_ord == 27:
                                    print("\r\n🔇 Escape pressed - stopping music...")
                                elif char_ord == 3:
                                    print("\r\n🔇 Ctrl+C pressed - stopping music...")
                                else:
                                    print("\r\n🔇 Q pressed - stopping music...")

                                self.stop_music(quiet=True)
                                self.stop_flag.set()
                                break
                    except (OSError, IOError):
                        # Handle any read errors
                        continue
        except Exception:
            pass
        finally:
            # Ensure terminal is always restored
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                pass

    def start_music_interactive(self):
        """Start music with escape key listener"""
        if self.is_music_playing():
            print("Elevator music is already playing")
            return

        self.start_music()
        if KEYBOARD_AVAILABLE:
            print("🎵 Press ESC or Q to stop music...")
            escape_thread = threading.Thread(target=self.listen_for_escape, daemon=True)
            escape_thread.start()
            try:
                while not self.stop_flag.is_set() and self.is_music_playing():
                    pass
            except KeyboardInterrupt:
                print("\n🔇 Interrupted - stopping music...")
                self.stop_music()
        else:
            print("🎵 Music started - use 'python claude_muzak.py stop' to stop")

    def run_with_music(self, command):
        """Run a command with elevator music playing"""
        self.start_music()
        try:
            if isinstance(command, str):
                process = subprocess.run(command, shell=True)
            else:
                process = subprocess.run(command)
            return process.returncode
        finally:
            self.stop_music()

    def hook(self, hook_type="start"):
        """Handle Claude Code hook integration"""
        if hook_type == "start":
            self.start_music(quiet=True)
            sys.stdout.flush()
            print(json.dumps({"allow": True}))
            sys.stdout.flush()
        elif hook_type == "stop":
            self.stop_music(quiet=True)
        return 0

def main():
    """
    Main entry point for the Claude Muzak application.

    Parses command line arguments and executes the appropriate music control action.
    """
    muzak = ClaudeMuzak()

    if len(sys.argv) < 2:
        print("🎵 Claude Muzak - Elevator music for your Claude Code tasks!")
        print()
        print("✨ Features:")
        print("   • Random music selection from your muzakfiles/ directory")
        print("   • Easy control with ESC, Q, or Ctrl+C")
        print("   • Automatic integration with Claude Code hooks")
        print()
        print("📖 Usage:")
        print("  python3 claude_muzak.py start           - Start music (press ESC or Q to stop)")
        print("  python3 claude_muzak.py stop            - Stop music")
        print("  python3 claude_muzak.py run <command>   - Run command with music")
        print("  python3 claude_muzak.py hook start      - Hook: start music")
        print("  python3 claude_muzak.py hook stop       - Hook: stop music")
        print()
        print("🚀 Quick setup: Create 'muzakfiles/' directory and add your music files!")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "start":
            muzak.start_music_interactive()
        elif command == "stop":
            muzak.stop_music()
        elif command == "run":
            if len(sys.argv) < 3:
                print("❌ Error: 'run' command requires a command to execute")
                print("   Example: python3 claude_muzak.py run 'npm test'")
                sys.exit(1)
            cmd_to_run = " ".join(sys.argv[2:])
            exit_code = muzak.run_with_music(cmd_to_run)
            sys.exit(exit_code)
        elif command == "hook":
            if len(sys.argv) < 3:
                print("❌ Error: 'hook' command requires start or stop")
                sys.exit(1)
            hook_type = sys.argv[2]
            if hook_type not in ["start", "stop"]:
                print("❌ Error: hook type must be 'start' or 'stop'")
                sys.exit(1)
            exit_code = muzak.hook(hook_type)
            sys.exit(exit_code)
        else:
            print(f"❌ Unknown command: {command}")
            print("   Run without arguments to see usage help")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🔇 Interrupted - stopping music...")
        muzak.stop_music()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()