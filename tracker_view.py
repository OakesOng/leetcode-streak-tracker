import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# --- Configuration for Cartoonish Theme (Basic Tkinter) ---
# Define color scheme for the GUI elements
BG_COLOR = '#ffe4b5'  # Misty Rose background
BUTTON_COLOR = '#98fb98' # Pale Green buttons
ACTIVE_BUTTON_COLOR = '#90ee90' # Light Green when button is pressed
GAME_OVER_COLOR = 'red' # Color for game over text
NEW_GAME_COLOR = '#add8e6' # Light Blue for the new game button

# Define font styles using a cartoonish font (ensure it's available on the system)
FONT_FAMILY = "Comic Sans MS" # Suggestion for a fun font
LARGE_FONT = (FONT_FAMILY, 16, 'bold')
NORMAL_FONT = (FONT_FAMILY, 12)
MESSAGE_FONT = (FONT_FAMILY, 10, 'italic')

class TrackerView:
    """
    Handles the graphical user interface (GUI) for the LeetCode streak tracker.
    Displays the streak, cheat days, progress, messages, and buttons.
    """
    def __init__(self, root):
        """
        Initializes the main application window and creates the GUI elements.
        """
        self.root = root
        self.root.title("LeetCode Streak Tracker")
        self.root.geometry("400x450") # Set a default window size
        self.root.configure(bg=BG_COLOR) # Set the background color of the window

        # Configure a style for themed widgets like the Progressbar
        style = ttk.Style()
        style.theme_use('clam') # Use the 'clam' theme for better styling options
        style.configure("TProgressbar",
                        background=BUTTON_COLOR, # Color of the filled part of the progress bar
                        troughcolor='lightgray', # Color of the unfilled part
                        bordercolor=BG_COLOR,
                        lightcolor=BUTTON_COLOR,
                        darkcolor=BUTTON_COLOR)

        # --- GUI Elements ---
        # Create and pack the labels, progress bar, and buttons

        # Label to display the current streak count
        self.streak_label = tk.Label(root, text="Streak: 0 days", font=LARGE_FONT, bg=BG_COLOR)
        self.streak_label.pack(pady=(20, 5))

        # Label to display the number of available cheat days
        self.cheat_label = tk.Label(root, text="Cheat Days: 0", font=NORMAL_FONT, bg=BG_COLOR)
        self.cheat_label.pack(pady=5)

        # Label for the progress bar description
        self.progress_label = tk.Label(root, text="Progress:", font=NORMAL_FONT, bg=BG_COLOR)
        self.progress_label.pack(pady=5)

        # Progress bar to visualize progress within a cycle
        # The maximum value will be set dynamically based on model configuration
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
        self.progress_bar.pack(pady=5)

        # Label to display messages (e.g., check-in results, milestones)
        self.message_label = tk.Label(root, text="", font=MESSAGE_FONT, bg=BG_COLOR, wraplength=350, justify="center")
        self.message_label.pack(pady=10)

        # Placeholder for image display (if implemented later)
        # self.image_label = tk.Label(root, bg=BG_COLOR)
        # self.image_label.pack(pady=10)
        # self.current_image = None # Keep a reference to avoid garbage collection

        # Button for the daily check-in action
        self.check_in_button = tk.Button(root, text="Check In Today", font=LARGE_FONT,
                                         command=lambda: self.check_in_callback(), # Command set by controller
                                         bg=BUTTON_COLOR, activebackground=ACTIVE_BUTTON_COLOR,
                                         padx=20, pady=10, relief=tk.RAISED)
        self.check_in_button.pack(pady=20)

        # Label to display "GAME OVER!" message
        self.game_over_label = tk.Label(root, text="", fg=GAME_OVER_COLOR, font=LARGE_FONT, bg=BG_COLOR)
        self.game_over_label.pack(pady=10)

        # Label to display game over statistics (e.g., highest streak)
        self.stats_label = tk.Label(root, text="", font=NORMAL_FONT, bg=BG_COLOR, wraplength=350, justify="center")
        self.stats_label.pack(pady=5)

        # Button to start a new game
        self.new_game_button = tk.Button(root, text="Start New Game", font=NORMAL_FONT,
                                         command=lambda: self.new_game_callback(), # Command set by controller
                                         bg=NEW_GAME_COLOR, activebackground=NEW_GAME_COLOR,
                                         padx=10, pady=5, relief=tk.RAISED)
        self.new_game_button.pack_forget() # Hide initially until game over

        # --- Callbacks ---
        # These will be set by the controller to link button clicks to controller methods
        self.check_in_callback = None
        self.new_game_callback = None

    def set_callbacks(self, check_in_cb, new_game_cb):
        """
        Method for the controller to assign the callback functions
        to the check-in and new game buttons.
        """
        self.check_in_callback = check_in_cb
        self.new_game_callback = new_game_cb

    def update_display(self, state):
        """
        Updates all GUI elements to reflect the current state of the tracker model.
        """
        # Update labels with current streak and cheat days
        self.streak_label.config(text=f"Streak: {state.streak_count} days")
        self.cheat_label.config(text=f"Cheat Days: {state.cheat_days}")

        # Update the progress bar based on the current streak and cycle
        self.progress_bar['maximum'] = state.PROGRESS_BAR_CYCLE # Ensure max is set from model config
        progress_value = state.streak_count % state.PROGRESS_BAR_CYCLE
        self.progress_bar['value'] = progress_value
        self.progress_label.config(text=f"Progress to {state.PROGRESS_BAR_CYCLE} day cycle: {progress_value}/{state.PROGRESS_BAR_CYCLE}")

        # Handle the display based on the game over state
        if state.is_game_over:
            # Disable check-in button and show game over elements
            self.check_in_button.config(state=tk.DISABLED)
            self.game_over_label.config(text="GAME OVER!")
            self.stats_label.config(text=f"Your highest streak in this game was: {state.highest_streak} days.") # Display highest streak stat
            self.new_game_button.pack(pady=10) # Show the new game button
        else:
            # If not game over, check if already checked in today to manage button state
            today = datetime.date.today()
            if state.last_check_in_date == today:
                 self.check_in_button.config(state=tk.DISABLED) # Disable if already checked in
            else:
                 self.check_in_button.config(state=tk.NORMAL) # Enable if not checked in

            # Hide game over elements
            self.game_over_label.config(text="")
            self.stats_label.config(text="")
            self.new_game_button.pack_forget() # Hide the new game button

        # Note: The message_label is updated separately by the controller's set_message method.

    def set_message(self, message):
         """
         Sets the text displayed in the main message label.
         """
         self.message_label.config(text=message)

    def show_confirmation(self, title, message):
        """
        Displays a yes/no confirmation message box and returns True for Yes, False for No.
        """
        return messagebox.askyesno(title, message)

    # Add methods here later if you implement image display (e.g., show_milestone_image)
