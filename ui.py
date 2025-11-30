import customtkinter as ctk
import json
import threading
from listener import VoiceListener

# Set theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")  # "green" gives a nice neon-ish vibe in dark mode

class GameVoiceMapperUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GameVoiceMapper - Command Center")
        self.geometry("500x700")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # The list area expands

        self.commands = self.load_commands()
        self.listener = VoiceListener(self.commands)
        self.is_listening = False

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="GAME VOICE MAPPER", 
            font=("Roboto Medium", 24, "bold"),
            text_color="#00FF00" # Neon Green
        )
        self.title_label.pack(pady=15)

        # --- Input Area ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        self.input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.input_frame, text="Voice Command:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.command_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 'shoot'")
        self.command_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.input_frame, text="Key Bind:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.key_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 'space' or 'ctrl+c'")
        self.key_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.input_frame, text="Duration (s):", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.duration_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. '0.5' (default 0.1)")
        self.duration_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.add_btn = ctk.CTkButton(
            self.input_frame, 
            text="ADD COMMAND", 
            command=self.add_command,
            fg_color="#1f538d", 
            hover_color="#14375e",
            font=("Arial", 12, "bold")
        )
        self.add_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="ew")

        # --- Command List Area ---
        self.list_label = ctk.CTkLabel(self, text="ACTIVE COMMANDS", font=("Arial", 14, "bold"))
        self.list_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 0))

        self.commands_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.commands_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        self.commands_frame.grid_columnconfigure(0, weight=1)

        # --- Footer / Controls ---
        self.footer_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        self.footer_frame.grid(row=4, column=0, sticky="ew", padx=0, pady=0)
        
        self.status_label = ctk.CTkLabel(self.footer_frame, text="STATUS: IDLE", text_color="gray", font=("Arial", 12, "bold"))
        self.status_label.pack(side="left", padx=20)

        self.listen_btn = ctk.CTkButton(
            self.footer_frame, 
            text="START LISTENING", 
            command=self.toggle_listening,
            fg_color="#2CC985",
            hover_color="#229965",
            font=("Arial", 14, "bold"),
            height=40
        )
        self.listen_btn.pack(side="right", padx=20, pady=20)

        self.refresh_command_list()

    def load_commands(self):
        try:
            with open("commands.json", "r") as f:
                return json.load(f)
        except:
            return {}

    def save_commands(self):
        with open("commands.json", "w") as f:
            json.dump(self.commands, f, indent=4)
        self.listener.update_commands(self.commands)

    def refresh_command_list(self):
        # Clear existing widgets in scrollable frame
        for widget in self.commands_frame.winfo_children():
            widget.destroy()

        for cmd, key in self.commands.items():
            self.create_command_card(cmd, key)

    def create_command_card(self, cmd, key_val):
        card = ctk.CTkFrame(self.commands_frame, fg_color="#2b2b2b")
        card.pack(fill="x", pady=5, padx=5)
        
        card.grid_columnconfigure(0, weight=1)
        
        # Parse display
        display_key = key_val
        display_dur = ""
        if ":" in key_val:
            parts = key_val.split(":")
            display_key = parts[0]
            display_dur = f" ({parts[1]}s)"

        info_label = ctk.CTkLabel(
            card, 
            text=f'"{cmd}"  ➜  [{display_key.upper()}]{display_dur}', 
            font=("Consolas", 14),
            anchor="w"
        )
        info_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        del_btn = ctk.CTkButton(
            card, 
            text="X", 
            width=30, 
            fg_color="#c42b1c", 
            hover_color="#8a1f14",
            command=lambda c=cmd: self.delete_command(c)
        )
        del_btn.grid(row=0, column=1, padx=10, pady=10)

    def add_command(self):
        cmd = self.command_entry.get().lower().strip()
        key = self.key_entry.get().lower().strip()
        duration = self.duration_entry.get().strip()

        if cmd and key:
            full_value = key
            if duration:
                try:
                    float(duration) # Validate
                    full_value = f"{key}:{duration}"
                except ValueError:
                    pass # Ignore invalid duration

            self.commands[cmd] = full_value
            self.save_commands()
            self.refresh_command_list()
            self.command_entry.delete(0, "end")
            self.key_entry.delete(0, "end")
            self.duration_entry.delete(0, "end")

    def delete_command(self, cmd):
        if cmd in self.commands:
            del self.commands[cmd]
            self.save_commands()
            self.refresh_command_list()

    def toggle_listening(self):
        if not self.is_listening:
            # Start
            self.is_listening = True
            self.listen_btn.configure(text="STOP LISTENING", fg_color="#c42b1c", hover_color="#8a1f14")
            self.status_label.configure(text="STATUS: LISTENING", text_color="#00FF00")
            
            # Start thread
            self.listen_thread = threading.Thread(target=self.listener.listen, daemon=True)
            self.listen_thread.start()
        else:
            # Stop
            self.is_listening = False
            self.listener.stop()
            self.listen_btn.configure(text="START LISTENING", fg_color="#2CC985", hover_color="#229965")
            self.status_label.configure(text="STATUS: IDLE", text_color="gray")
