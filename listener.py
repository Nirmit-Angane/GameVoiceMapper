import vosk
import os
import pyaudio
import json
import threading
import sys
from actions import press_key

class VoiceListener:
    def __init__(self, commands):
        self.commands = commands
        self.running = False
        self.lock = threading.Lock()
        
        # Execution management
        self.execution_thread = None
        self.stop_event = threading.Event()
        
        # Vosk initialization
        vosk.SetLogLevel(-1) # Silence logs
        try:
            if not os.path.exists("model"):
                 print("CRITICAL ERROR: 'model' directory not found. Please run download_model.py")
                 self.model = None
            else:
                print("Loading Vosk model... (this may take a moment)")
                self.model = vosk.Model("model")
                self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
                print("Vosk model loaded.")
        except Exception as e:
            print(f"Error loading Vosk model: {e}")
            self.model = None

    def update_commands(self, new_commands):
        self.commands = new_commands

    def listen(self):
        if not self.model:
            print("Model not loaded. Cannot listen.")
            return

        # Ensure only one listen loop runs at a time
        with self.lock:
            self.running = True
            
            p = pyaudio.PyAudio()
            try:
                stream = p.open(format=pyaudio.paInt16, 
                                channels=1, 
                                rate=16000, 
                                input=True, 
                                frames_per_buffer=8000)
                stream.start_stream()
                
                print("\nListening (Offline Mode)...")
                print("Speak a command!")
                
                while self.running:
                    try:
                        data = stream.read(4000, exception_on_overflow=False)
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "")
                            if text:
                                self.process_text(text)
                    except Exception as e:
                        print(f"Error in listener loop: {e}")
                        
                stream.stop_stream()
                stream.close()
            except Exception as e:
                print(f"Error initializing audio stream: {e}")
                if "[Errno -9999]" in str(e):
                    print("\nCRITICAL ERROR: Microphone access denied.")
                    print("Check Windows Privacy Settings > Microphone.")
            finally:
                p.terminate()
                self.running = False
                print("Listening stopped.")

    def process_text(self, text):
        print(f"Recognized: {text}")
        
        if text in self.commands:
            command_val = self.commands[text]
            print(f"Executing command: {text} -> {command_val}")
            self.execute_command(command_val)
        else:
            # Check for repeated commands (e.g., "left left left")
            words = text.split()
            for word in words:
                if word in self.commands:
                    command_val = self.commands[word]
                    print(f"Executing repeated command: {word} -> {command_val}")
                    self.execute_command(command_val)

    def stop(self):
        self.running = False

    def execute_command(self, command_val):
        # 1. Stop any running command
        if self.execution_thread and self.execution_thread.is_alive():
            print("Interrupting previous command...")
            self.stop_event.set()
            self.execution_thread.join() # Wait for it to finish cleaning up
            
        # 2. Reset event and start new thread
        self.stop_event.clear()
        self.execution_thread = threading.Thread(
            target=self._run_command_thread, 
            args=(command_val,), 
            daemon=True
        )
        self.execution_thread.start()

    def _run_command_thread(self, command_val):
        # Treat as single command (Combo feature removed)
        step = command_val.strip()
        if not step:
            return
            
        # Parse duration if present (e.g., "w:2.5")
        key_to_press = step
        duration = 0.1
        
        if ":" in step:
            try:
                parts = step.split(":")
                key_to_press = parts[0].strip()
                duration = float(parts[1])
            except ValueError:
                print(f"Invalid duration format in: {step}")
        
        print(f"  -> Pressing: {key_to_press} for {duration}s")
        press_key(key_to_press, duration, self.stop_event)
