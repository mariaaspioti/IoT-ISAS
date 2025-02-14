import os
import sys
import glob
import signal
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk

class SystemManager:
    def __init__(self):
        self.processes = []
        self.agents = {}
        self.root_dir = Path(__file__).parent.resolve()
        self.source_dir = self.root_dir / "source"
        self.iot_dir = self.source_dir / "IoT-devices"

        if not self.iot_dir.exists():
            raise FileNotFoundError(f"IoT-devices directory not found at {self.iot_dir}")

        self.iot_agent_files = sorted(glob.glob(str(self.iot_dir / "IoTAgent-*.py")))
        self.required_devices = ["beacon_mimic.py", "button_mimic.py"]
        self.nfc_reader_file = self.iot_dir / "nfc_reader_mimic.py"
        self.npm_process = None

    def is_agent_running(self, agent_path):
        return agent_path in self.agents

    def start_agent(self, agent_path):
        if not self.is_agent_running(agent_path):
            self._start_agent(agent_path)

    def stop_agent(self, agent_path):
        if self.is_agent_running(agent_path):
            self._stop_process(agent_path)

    def start_all_agents(self):
        """Start all IoT agents and required mock devices."""
        # Start IoT Agents
        for agent_path in self.iot_agent_files:
            self._start_agent(agent_path)

        # Start required mock devices
        for device in self.required_devices:
            device_path = str(self.iot_dir / device)
            self._start_agent(device_path)

        # Start optional NFC reader if it exists
        if self.nfc_reader_file.exists():
            self._start_agent(str(self.nfc_reader_file))

    def stop_all_agents(self):
        """Stop all currently running IoT agent processes."""
        for agent_path, proc in list(self.agents.items()):
            self._stop_process(agent_path)
        self.agents.clear()

    def reload_agent(self, agent_path):
        """Stop and then restart a specific IoT agent."""
        self._stop_process(agent_path)
        self._start_agent(agent_path)

    def start_system(self):
        """Start all components (agents + server)."""
        self.start_all_agents()
        self.start_npm_server()

    def shutdown(self):
        """Terminate all running processes (agents + npm)."""
        print("Shutting down all processes...")
        self.stop_all_agents()
        self.stop_npm_server()
        print("All processes stopped.")

    def _start_agent(self, agent_path):
        """Helper to start a single agent process."""
        if agent_path in self.agents:
            print(f"Agent already running: {agent_path}")
            return

        try:
            proc = subprocess.Popen(
                [sys.executable, agent_path],
                stdout=sys.stdout,
                stderr=sys.stderr
            )
            self.agents[agent_path] = proc
            self.processes.append(proc)
            print(f"Started agent: {agent_path}")
        except Exception as e:
            print(f"Error starting {agent_path}: {str(e)}")

    def _stop_process(self, agent_path):
        """Helper to stop a single agent process."""
        proc = self.agents.get(agent_path)
        if proc is not None:
            try:
                print(f"Stopping agent: {agent_path}")
                proc.terminate()
                proc.wait(timeout=5)
            except Exception as e:
                print(f"Error terminating agent {agent_path}: {str(e)}")
            finally:
                if proc in self.processes:
                    self.processes.remove(proc)
                del self.agents[agent_path]

    def start_npm_server(self):
        """Start the Node.js server via npm."""
        npm_cmd = ["npm", "run", "install-start:all"]
        try:
            shell_flag = sys.platform == "win32"
            self.npm_process = subprocess.Popen(
                npm_cmd,
                cwd=str(self.source_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=shell_flag,
                preexec_fn=os.setsid if sys.platform == "win32" else None   
            )
            self.processes.append(self.npm_process)
            print(f"Started Node.js server in {self.source_dir}")
        except Exception as e:
            print(f"Error starting npm server: {str(e)}")
            print(f"Command attempted: {' '.join(npm_cmd)}")
            print(f"Working directory: {self.source_dir}")

    def stop_npm_server(self):
        """Stop the Node.js server if it's running."""
        if self.npm_process:
            try:
                print("Stopping Node.js server (npm).")
                # self.npm_process.terminate()
                # On Windows, send CTRL_BREAK_EVENT to the process group
                self.npm_process.send_signal(signal.CTRL_BREAK_EVENT)
                self.npm_process.wait(timeout=5)
            except Exception as e:
                print(f"Error terminating npm server: {str(e)}")
            finally:
                if self.npm_process in self.processes:
                    self.processes.remove(self.npm_process)
                self.npm_process = None

    def install_npm_dependencies(self):
        """Run npm install to install dependencies."""
        npm_cmd = ["npm", "install"]
        try:
            shell_flag = sys.platform == "win32"
            install_process = subprocess.Popen(
                npm_cmd,
                cwd=str(self.source_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=shell_flag
            )
            self.processes.append(install_process)
            print(f"Running npm install in {self.source_dir}")
            return True
        except Exception as e:
            print(f"Error running npm install: {str(e)}")
            return False


class GUIManager:
    def __init__(self, system_manager):
        self.system_manager = system_manager
        self.root = tk.Tk()
        self.root.title("IoT System Manager")
        self.agent_widgets = {}

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ========== CONTROL FRAME FOR NPM AND AGENTS ==========
        control_frame = ttk.LabelFrame(main_frame, text="Global Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)

        # NPM (server) controls
        ttk.Button(control_frame, text="Start Server", command=self.start_server).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Server", command=self.stop_server).pack(side=tk.LEFT, padx=5)

        # Agent controls
        ttk.Button(control_frame, text="Start Agents", command=self.start_agents).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Agents", command=self.stop_agents).pack(side=tk.LEFT, padx=5)

        # Combined controls
        ttk.Button(control_frame, text="Start All", command=self.start_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop All", command=self.stop_all).pack(side=tk.LEFT, padx=5)

        # ========== INSTALL FRAME ==========
        install_frame = ttk.LabelFrame(main_frame, text="Installation", padding="10")
        install_frame.pack(fill=tk.X, pady=5)
        ttk.Button(install_frame, text="Install NPM Dependencies", command=self.install_npm).pack(side=tk.LEFT, padx=5)

        # ========== AGENT LIST ==========
        list_frame = ttk.LabelFrame(main_frame, text="Agents & Devices", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Create agent rows (IoT Agents)
        self.create_agent_rows(list_frame, "IoT Agents:", self.system_manager.iot_agent_files)
        # Required devices
        faker_paths = [str(self.system_manager.iot_dir / d) for d in self.system_manager.required_devices]
        self.create_agent_rows(list_frame, "Fakers:", faker_paths)
        # NFC reader if it exists
        if self.system_manager.nfc_reader_file.exists():
            self.create_agent_rows(list_frame, "NFC Reader:", [str(self.system_manager.nfc_reader_file)])

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # -------------- BUTTON HANDLERS --------------

    def install_npm(self):
        """Handle npm install button click"""
        success = self.system_manager.install_npm_dependencies()
        if success:
            self.show_status("Running npm install... Check console for progress.")
        else:
            self.show_status("Failed to start npm install!", error=True)

    def start_server(self):
        self.system_manager.start_npm_server()
        self.show_status("Server started.")

    def stop_server(self):
        self.system_manager.stop_npm_server()
        self.show_status("Server stopped.")

    def start_agents(self):
        self.system_manager.start_all_agents()
        self.refresh_all_buttons()
        self.show_status("All agents started.")

    def stop_agents(self):
        self.system_manager.stop_all_agents()
        self.refresh_all_buttons()
        self.show_status("All agents stopped.")

    def start_all(self):
        self.system_manager.start_system()  # Agents + server
        self.refresh_all_buttons()
        self.show_status("System started (all agents + server).")

    def stop_all(self):
        self.system_manager.shutdown()  # Agents + server
        self.refresh_all_buttons()
        self.show_status("System stopped.")

    # -------------- UI HELPERS --------------

    def create_agent_rows(self, parent, section_title, items):
        """Create a row for each agent/device file, with a Start/Stop button."""
        if not items:
            return

        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=5)

        ttk.Label(section_frame, text=section_title, font=('Arial', 9, 'bold')).pack(anchor=tk.W)

        for path in items:
            row_frame = ttk.Frame(parent)
            row_frame.pack(fill=tk.X, pady=2)

            label_text = os.path.basename(path)
            ttk.Label(row_frame, text=label_text).pack(side=tk.LEFT, padx=5)

            btn = ttk.Button(
                row_frame,
                text="Start" if not self.system_manager.is_agent_running(path) else "Stop",
                command=lambda p=path: self.toggle_agent(p)
            )
            btn.pack(side=tk.RIGHT, padx=5)

            self.agent_widgets[path] = {'button': btn, 'label': label_text}

    def toggle_agent(self, agent_path):
        """Toggle a single agent on/off."""
        if self.system_manager.is_agent_running(agent_path):
            self.system_manager.stop_agent(agent_path)
        else:
            self.system_manager.start_agent(agent_path)
        self.update_button_state(agent_path)

    def update_button_state(self, agent_path):
        btn = self.agent_widgets[agent_path]['button']
        btn.config(text="Stop" if self.system_manager.is_agent_running(agent_path) else "Start")

    def refresh_all_buttons(self):
        """Refresh the Start/Stop text for all agent buttons."""
        for agent_path in self.agent_widgets:
            self.update_button_state(agent_path)

    def show_status(self, message, error=False):
        """Display a status message at the bottom of the window."""
        status_color = "#ff0000" if error else "#006600"
        status_label = ttk.Label(self.root, text=message, foreground=status_color)
        status_label.pack(pady=5)
        # Remove status after 5 seconds
        self.root.after(5000, status_label.destroy)

    def on_close(self):
        # Gracefully shut down everything before closing
        self.system_manager.shutdown()
        self.root.destroy()

    def run(self):
        # Start the Tk event loop
        self.root.mainloop()


if __name__ == "__main__":
    try:
        manager = SystemManager()
        gui = GUIManager(manager)
        gui.run()
    except Exception as e:
        print(f"System startup failed: {str(e)}")
        sys.exit(1)
