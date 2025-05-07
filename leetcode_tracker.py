import tkinter as tk
from tracker_model import TrackerState
from tracker_view import TrackerView
from tracker_controller import TrackerController

if __name__ == "__main__":
    root = tk.Tk()

    # Initialize Model, View, and Controller
    model = TrackerState()
    view = TrackerView(root)
    controller = TrackerController(model, view)

    # Set up the protocol to call controller.on_closing when the window is closed
    root.protocol("WM_DELETE_WINDOW", controller.on_closing)

    # Start the Tkinter event loop
    root.mainloop()