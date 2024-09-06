import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, END
import customtkinter as ctk
import os
import json
import pygetwindow as gw
import keyboard
import pystray
from workspace import Workspace
from utils import get_screen_size, ToolTip
from config import WINDOW_SIZE 
from PIL import Image


# WorkspaceApp class to manage the GUI and workspace operations
# This class will be used to create the main application window and manage the workspaces
# It will handle the creation, loading, and running of workspaces, as well as the snapper feature

class WorkspaceApp:
    """_summary_
    """    
    def __init__(self, root):
        self.root = root
        self.root.title("Workspaces 2.0")
        self.root.geometry(WINDOW_SIZE)  
        self.root.protocol("WM_DELETE_WINDOW", self.minimise_to_tray)
        
        self.workspaces = {}
        self.current_workspace = None

        # Variable to track the state of the snapper feature
        self.feature_enabled = tk.BooleanVar(value=False)

        # Main Menu Frame
        self.main_menu_frame = ctk.CTkFrame(root)
        self.main_menu_frame.pack(fill=ctk.BOTH, expand=True)

        self.workspace_name_var = ctk.StringVar()

        self.create_workspace_button = ctk.CTkButton(self.main_menu_frame, text="Create Workspace", command=self.create_workspace)
        self.create_workspace_button.pack(pady=10)

        self.rename_workspace_button = ctk.CTkButton(self.main_menu_frame, text="Rename Workspace", command=self.rename_workspace)
        self.rename_workspace_button.pack(pady=10)

        self.load_workspace_button = ctk.CTkButton(self.main_menu_frame, text="Import Workspace", command=self.import_workspace)
        self.load_workspace_button.pack(pady=10)

        self.workspace_listbox = Listbox(self.main_menu_frame)
        self.workspace_listbox.pack(fill=ctk.BOTH, expand=True, pady=10)
        self.workspace_listbox.bind('<Double-1>', self.open_workspace)
        
        self.minimise = ctk.CTkButton(self.main_menu_frame, text="minimise", command=self.minimise_to_tray)
        self.minimise.pack(pady=10)

        # Snapper Feature Switch
        self.snapper_switch = ctk.CTkSwitch(self.main_menu_frame, text="Window Snapper", command=self.toggle_feature, variable=self.feature_enabled)
        self.snapper_switch.pack(pady=10)

        # Add Tooltip to Snapper Switch
        tooltip_text = ("Ctrl + F1: Snap Left\n"
                        "Ctrl + F2: Snap Right\n"
                        "Ctrl + F3: Snap Top Left\n"
                        "Ctrl + F4: Snap Top Right\n"
                        "Ctrl + F5: Snap Bottom Left\n"
                        "Ctrl + F6: Snap Bottom Right")
        ToolTip(self.snapper_switch, tooltip_text)

        # Workspace Details Frame
        self.workspace_frame = ctk.CTkFrame(root)

        self.back_button = ctk.CTkButton(self.workspace_frame, text="Back", command=self.show_main_menu)
        self.back_button.pack(pady=10)

        self.action_listbox = Listbox(self.workspace_frame)
        self.action_listbox.pack(fill=ctk.BOTH, expand=True, pady=10)

        self.add_app_button = ctk.CTkButton(self.workspace_frame, text="Add Application", command=self.add_application)
        self.add_app_button.pack(pady=5)

        self.add_url_button = ctk.CTkButton(self.workspace_frame, text="Add URL", command=self.add_url)
        self.add_url_button.pack(pady=5)

        self.add_file_button = ctk.CTkButton(self.workspace_frame, text="Add File", command=self.add_file)
        self.add_file_button.pack(pady=5)

        self.add_folder_button = ctk.CTkButton(self.workspace_frame, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack(pady=5)

        self.add_script_button = ctk.CTkButton(self.workspace_frame, text="Add Script", command=self.add_script)
        self.add_script_button.pack(pady=5)

        self.move_up_button = ctk.CTkButton(self.workspace_frame, text="Move Action Up", command=self.move_action_up)
        self.move_up_button.pack(pady=5)

        self.move_down_button = ctk.CTkButton(self.workspace_frame, text="Move Action Down", command=self.move_action_down)
        self.move_down_button.pack(pady=5)

        self.remove_action_button = ctk.CTkButton(self.workspace_frame, text="Remove Action", command=self.remove_action)
        self.remove_action_button.pack(pady=10)

        self.run_workspace_button = ctk.CTkButton(self.workspace_frame, text="Run Workspace", command=self.run_workspace)
        self.run_workspace_button.pack(pady=10)

        # Automatically load workspaces from JSON files in the current directory
        self.load_existing_workspaces()

        # Initially show main menu
        self.show_main_menu()

        # Bind hotkeys for snapping to different quadrants
        keyboard.add_hotkey('ctrl+f1', self.snap_window_left)
        keyboard.add_hotkey('ctrl+f2', self.snap_window_right)
        keyboard.add_hotkey('ctrl+f3', self.snap_window_top_left)
        keyboard.add_hotkey('ctrl+f4', self.snap_window_top_right)
        keyboard.add_hotkey('ctrl+f5', self.snap_window_bottom_left)
        keyboard.add_hotkey('ctrl+f6', self.snap_window_bottom_right)


    # Main Menu Buttons 
    def create_workspace(self):
        dialog = ctk.CTkInputDialog(text="Enter Workspace Name:", title="Create Workspace")
        name = dialog.get_input()
        if name:
            if name not in self.workspaces:
                self.workspaces[name] = Workspace(name)
                self.workspaces[name].save()  # Save initial workspace
                self.update_workspace_listbox()
            else:
                messagebox.showwarning("Warning", "Workspace already exists!")

    def rename_workspace(self):
        selected = self.get_selected_workspace()
        if selected:
            current_name = selected
            dialog = ctk.CTkInputDialog(text="New Workspace Name:", title="Rename Workspace")
            new_name = dialog.get_input()
            if new_name and new_name != current_name:
                if new_name not in self.workspaces:
                    # Rename workspace and update the list
                    self.workspaces[current_name].rename(new_name)
                    self.workspaces[new_name] = self.workspaces.pop(current_name)
                    self.update_workspace_listbox()
                else:
                    messagebox.showwarning("Warning", f"Workspace '{new_name}' already exists.")
            elif new_name == current_name:
                messagebox.showinfo("Info", "The new name is the same as the current name.")
            else:
                messagebox.showwarning("Warning", "No new name provided.")

    # Import work space
    def import_workspace(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                actions = json.load(f)
                # Extract the workspace name from the file path
                name = os.path.splitext(os.path.basename(file_path))[0]

                # Validate the imported JSON structure
                if isinstance(actions, list) and all(isinstance(action, dict) and 'type' in action and 'action' in action for action in actions):
                    if name not in self.workspaces:
                        # Create a new workspace with the imported actions
                        workspace = Workspace(name)
                        workspace.actions = actions
                        workspace.save()  # Save the imported workspace into the current directory
                        self.workspaces[name] = workspace
                        self.update_workspace_listbox()
                    else:
                        messagebox.showwarning("Warning", f"Workspace '{name}' already exists.")
                else:
                    messagebox.showerror("Error", "Invalid JSON structure. Ensure the file contains a list of actions with 'type' and 'action' keys.")

    # Load existing workspaces (json files) in the current directory
    def load_existing_workspaces(self):
        # Get the directory where the script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Loop through all JSON files in the current directory
        for filename in os.listdir(current_dir):
            if filename.endswith(".json"):
                name = os.path.splitext(filename)[0]
                workspace = Workspace(name)
                workspace.load()  # Load the actions from the JSON file
                self.workspaces[name] = workspace

        # Update the workspace listbox to reflect the loaded workspaces
        self.update_workspace_listbox()

    def update_workspace_listbox(self):
        self.workspace_listbox.delete(0, END)
        for name in self.workspaces:
            self.workspace_listbox.insert(END, name)

    def get_selected_workspace(self):
        selected = self.workspace_listbox.curselection()
        if selected:
            return self.workspace_listbox.get(selected[0])
        else:
            messagebox.showwarning("Warning", "No workspace selected.")
            return None

    def open_workspace(self, event):
        selected = self.get_selected_workspace()
        if selected:
            self.current_workspace = selected
            self.workspaces[self.current_workspace].load()  # Load the workspace actions from JSON file
            self.update_action_listbox()
            self.show_workspace_frame()

    def show_main_menu(self):
        self.workspace_frame.pack_forget()
        self.main_menu_frame.pack(fill=ctk.BOTH, expand=True)

    def show_workspace_frame(self):
        self.main_menu_frame.pack_forget()
        self.workspace_frame.pack(fill=ctk.BOTH, expand=True)

    # Within a Workspace Frame Buttons

    def add_application(self):
        app_path = filedialog.askopenfilename(filetypes=[("Applications", "*.exe")])
        if app_path and self.current_workspace:
            self.workspaces[self.current_workspace].add_action("application", app_path)
            self.update_action_listbox()

    def add_url(self):
        dialog = ctk.CTkInputDialog(text="Enter URL:", title="Add URL")
        url = dialog.get_input()
        if url and self.current_workspace:
            self.workspaces[self.current_workspace].add_action("url", url)
            self.update_action_listbox()

    def add_file(self):
        file_path = filedialog.askopenfilename()
        if file_path and self.current_workspace:
            self.workspaces[self.current_workspace].add_action("file", file_path)
            self.update_action_listbox()

    def add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path and self.current_workspace:
            self.workspaces[self.current_workspace].add_action("folder", folder_path)
            self.update_action_listbox()

    def add_script(self):
        script_path = filedialog.askopenfilename(filetypes=[("Scripts", "*.ps1 *.py *.sh *.bat")])
        if script_path and self.current_workspace:
            self.workspaces[self.current_workspace].add_action("script", script_path)
            self.update_action_listbox()

    def move_action_up(self):
        selected = self.get_selected_action()
        if selected:
            index = int(selected.split(":")[0])
            if index > 0:
                self.workspaces[self.current_workspace].move_action_up(index)
                self.update_action_listbox()

    def move_action_down(self):
        selected = self.get_selected_action()
        if selected:
            index = int(selected.split(":")[0])
            if index < len(self.workspaces[self.current_workspace].actions) - 1:
                self.workspaces[self.current_workspace].move_action_down(index)
                self.update_action_listbox()

    def remove_action(self):
        selected = self.get_selected_action()
        if selected and self.current_workspace:
            index = int(selected.split(":")[0])
            self.workspaces[self.current_workspace].remove_action(index)
            self.update_action_listbox()

    def run_workspace(self):
        if self.current_workspace:
            self.workspaces[self.current_workspace].run()

    def update_action_listbox(self):
        self.action_listbox.delete(0, END)
        if self.current_workspace:
            for i, action in enumerate(self.workspaces[self.current_workspace].actions):
                self.action_listbox.insert(END, f"{i}: {action['type']}: {action['action']}")

    def get_selected_action(self):
        selected = self.action_listbox.curselection()
        if selected:
            return self.action_listbox.get(selected[0])
        else:
            messagebox.showwarning("Warning", "No action selected.")
            return None

    # Toggle the snapper feature using CustomTkinter switch
    def toggle_feature(self):
        if self.feature_enabled.get():
            print("Snapper Feature enabled")
        else:
            print("Snapper Feature disabled")

    # Snap the active window to the left half of the screen
    def snap_window_left(self):
        if self.feature_enabled.get():
            active_window = gw.getActiveWindow()
            if active_window:
                screen_width, screen_height = get_screen_size()
                active_window.moveTo(0, 0)
                active_window.resizeTo(screen_width // 2, screen_height)
                print("Window snapped to the left half of the screen")
            else:
                print("No active window found")

    # Snap the active window to the right half of the screen
    def snap_window_right(self):
        if self.feature_enabled.get():
            active_window = gw.getActiveWindow()
            if active_window:
                screen_width, screen_height = get_screen_size()
                active_window.moveTo(screen_width // 2, 0)
                active_window.resizeTo(screen_width // 2, screen_height)
                print("Window snapped to the right half of the screen")
            else:
                print("No active window found")

    # Snap the active window to the top-left quadrant of the screen
    def snap_window_top_left(self):
        if self.feature_enabled.get():
            active_window = gw.getActiveWindow()
            if active_window:
                screen_width, screen_height = get_screen_size()
                active_window.moveTo(0, 0)
                active_window.resizeTo(screen_width // 2, screen_height // 2)
                print("Window snapped to the top-left quadrant")
            else:
                print("No active window found")

    # Snap the active window to the top-right quadrant of the screen
    def snap_window_top_right(self):
        if self.feature_enabled.get():
            active_window = gw.getActiveWindow()
            if active_window:
                screen_width, screen_height = get_screen_size()
                active_window.moveTo(screen_width // 2, 0)
                active_window.resizeTo(screen_width // 2, screen_height // 2)
                print("Window snapped to the top-right quadrant")
            else:
                print("No active window found")

    # Snap the active window to the bottom-left quadrant of the screen
    def snap_window_bottom_left(self):
        if self.feature_enabled.get():
            active_window = gw.getActiveWindow()
            if active_window:
                screen_width, screen_height = get_screen_size()
                active_window.moveTo(0, screen_height // 2)
                active_window.resizeTo(screen_width // 2, screen_height // 2)
                print("Window snapped to the bottom-left quadrant")
            else:
                print("No active window found")

    # Snap the active window to the bottom-right quadrant of the screen
    def snap_window_bottom_right(self):
        if self.feature_enabled.get():
            active_window = gw.getActiveWindow()
            if active_window:
                screen_width, screen_height = get_screen_size()
                active_window.moveTo(screen_width // 2, screen_height // 2)
                active_window.resizeTo(screen_width // 2, screen_height // 2)
                print("Window snapped to the bottom-right quadrant")
            else:
                print("No active window found")
    
    def minimise_to_tray(self):
        self.root.withdraw()
        image = Image.open("app.ico")
        menu = (
            pystray.MenuItem("Maximise", self.maximise_from_tray),
            pystray.MenuItem("Quit", self.close_application)
        )
        self.icon = pystray.Icon("name", image, "MyApp", menu)
        self.icon.run()

    def maximise_from_tray(self):
        self.icon.stop()
        self.root.after(0, self.root.deiconify)

    def close_application(self):
        self.icon.stop()
        self.root.destroy()
