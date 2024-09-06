import json
import os
import subprocess
import webbrowser

# Workspace class to manage actions
# Actions can be of type application, url, file, folder, or script
# Actions are stored in a JSON file
# Actions can be added, removed, moved up, moved down, and run

class Workspace:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.filename = f"{name}.json"

    def add_action(self, action_type, action):
        self.actions.append({"type": action_type, "action": action})
        self.save()

    def remove_action(self, index):
        if 0 <= index < len(self.actions):
            self.actions.pop(index)
            self.save()

    def move_action_up(self, index):
        if index > 0:
            self.actions[index - 1], self.actions[index] = self.actions[index], self.actions[index - 1]
            self.save()

    def move_action_down(self, index):
        if index < len(self.actions) - 1:
            self.actions[index + 1], self.actions[index] = self.actions[index], self.actions[index + 1]
            self.save()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.actions, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.actions = json.load(f)

    def rename(self, new_name):
        new_filename = f"{new_name}.json"
        os.rename(self.filename, new_filename)
        self.name = new_name
        self.filename = new_filename

    def run(self):
        for action in self.actions:
            if action["type"] == "application":
                subprocess.Popen(action["action"])
            elif action["type"] == "url":
                webbrowser.open(action["action"])
            elif action["type"] == "file":
                os.startfile(action["action"])
            elif action["type"] == "folder":
                os.startfile(action["action"])
            elif action["type"] == "script":
                self.run_script(action["action"])

    def run_script(self, script_path):
        extension = os.path.splitext(script_path)[1].lower()
        if extension == ".ps1":
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path])
        elif extension == ".py":
            subprocess.run(["python", script_path])
        elif extension in [".sh", ".bat"]:
            subprocess.run([script_path], shell=True)
        else:
            print(f"Unsupported script type: {extension}")
    
