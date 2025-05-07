import tkinter as tk
import datetime
# Import the Model and View components
from tracker_model import TrackerState
from tracker_view import TrackerView

class TrackerController:
    """
    Handles the interaction logic between the TrackerState (Model)
    and the TrackerView (GUI).
    """
    def __init__(self, model: TrackerState, view: TrackerView):
        self.model = model
        self.view = view

        # Set up the command callbacks for buttons in the view
        self.view.set_callbacks(self.handle_check_in, self.handle_new_game)

        # Load the saved state when the application starts
        self.model.load()

        # Update the GUI display based on the loaded state
        self.update_view()

        # After loading and updating the view, check if the user already checked in today
        today = datetime.date.today()
        if self.model.last_check_in_date == today and not self.model.is_game_over:
             self.view.set_message("You have already checked in today.")
             # Disable the check-in button if already checked in today
             self.view.check_in_button.config(state=tk.DISABLED)

    def handle_check_in(self):
        """
        Handles the logic when the 'Check In Today' button is clicked.
        Updates the model state and refreshes the view.
        """
        # Call the model's check_in method to process the check-in
        result_message = self.model.check_in()

        # Update the message display in the view with the result
        self.view.set_message(result_message)

        # Refresh the entire view to reflect the updated model state
        self.update_view()

        # Return the message for potential use (e.g., in testing)
        return result_message

    def handle_new_game(self):
        """
        Handles the logic when the 'Start New Game' button is clicked.
        Prompts for confirmation, resets the model state, and refreshes the view.
        """
        # Show a confirmation dialog before starting a new game
        if self.view.show_confirmation("Start New Game", "Are you sure you want to start a new game? Your current progress (streak, cheat days) will be reset, but your highest streak record will remain."):
            # Reset the model state for a new game
            self.model.start_new_game()
            # Set a message indicating the new game has started
            self.view.set_message("New game started! Good luck!")
            # Refresh the view to show the reset state
            self.update_view()
            # Re-enable the check-in button for the new game
            self.view.check_in_button.config(state=tk.NORMAL)
            # Return a message indicating new game started for potential testing
            return "New game started! Good luck!"
        else:
            # Return a message indicating new game cancelled for potential testing
            return "New game cancelled."


    def update_view(self):
        """
        Instructs the view to update its display based on the current state of the model.
        """
        self.view.update_display(self.model)

    def on_closing(self):
        """
        Handles the application closing event. Saves the current state before exiting.
        """
        self.model.save()
        # Destroy the Tkinter window to close the application
        self.view.root.destroy()
