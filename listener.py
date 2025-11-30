import speech_recognition as sr
import threading
from actions import press_key

class VoiceListener:
    def __init__(self, commands):
        self.commands = commands
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.running = False
        self.lock = threading.Lock()

    def update_commands(self, new_commands):
        self.commands = new_commands

    def listen(self):
        # Ensure only one listen loop runs at a time
        with self.lock:
            self.running = True
            
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    print("Listening started...")
                    
                    while self.running:
                        try:
                            # Listen with a short timeout to allow checking self.running
                            try:
                                audio_data = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                            except sr.WaitTimeoutError:
                                continue
                            
                            text = self.recognizer.recognize_google(audio_data).lower().strip()
                            print(f"Recognized: {text}")

                            if text in self.commands:
                                command_val = self.commands[text]
                                print(f"Executing command: {text} -> {command_val}")
                                
                                # Parse duration if present (e.g., "w:2.5")
                                key_to_press = command_val
                                duration = 0.1
                                
                                if ":" in command_val:
                                    try:
                                        parts = command_val.split(":")
                                        key_to_press = parts[0]
                                        duration = float(parts[1])
                                    except ValueError:
                                        print(f"Invalid duration format in: {command_val}")
                                
                                press_key(key_to_press, duration)

                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print(f"Could not request results; {e}")
                        except Exception as e:
                            print(f"Error in listener loop: {e}")
                            
            except Exception as e:
                print(f"Error initializing listener: {e}")
            finally:
                self.running = False
                print("Listening stopped.")

    def stop(self):
        self.running = False
