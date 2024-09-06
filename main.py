import tkinter as tk
import customtkinter as ctk
from workspace_app import WorkspaceApp

# This is the main file that runs the application.
if __name__ == "__main__":
    root = ctk.CTk()
    app = WorkspaceApp(root)
    root.mainloop()
