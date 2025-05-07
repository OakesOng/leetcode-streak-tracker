import json
import datetime
import os

# Define the file name for saving and loading the tracker state
STATE_FILE = "leetcode_tracker_state.json"

class TrackerState:
    """
    Manages the state of the LeetCode streak tracker, including streak count,
    cheat days, last check-in date, game over status, and highest streak.
    Handles saving and loading the state to a JSON file.
    """
    def __init__(self):
        # Initialize the tracker state attributes
        self.streak_count = 0
        self.cheat_days = 0
        self.last_check_in_date = None # Stores the date of the last successful check-in
        self.is_game_over = False
        self.highest_streak = 0 # Tracks the longest streak achieved in a single game

        # --- Configuration ---
        # Rate at which cheat days are earned (e.g., 1 cheat day every 14 streak days)
        self.CHEAT_DAY_EARN_RATE = 14
        # The maximum value for the progress bar before it cycles
        self.PROGRESS_BAR_CYCLE = 30
        # Define milestones for motivational messages/images (streak count: message/key)
        self.MILESTONES = {
            7: "Week 1 done! Keep pushing!",
            30: "One month solid! Amazing!",
            100: "Century Streak! You're a coding machine!",
            # Add more milestones and messages/image keys here
            # Example: 60: {"message": "Two months!", "image": "path/to/image.png"}
        }
        # --- End Configuration ---

    def load(self):
        """
        Loads the tracker state from the STATE_FILE if it exists.
        If the file is not found or is corrupted, resets the state to default.
        """
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    state_data = json.load(f)
                    self.streak_count = state_data.get('streak_count', 0)
                    self.cheat_days = state_data.get('cheat_days', 0)
                    last_date_str = state_data.get('last_check_in_date')
                    if last_date_str:
                        # Convert the date string back to a datetime.date object
                        self.last_check_in_date = datetime.date.fromisoformat(last_date_str)
                    else:
                        self.last_check_in_date = None # Handle cases where the date was not saved
                    self.is_game_over = state_data.get('is_game_over', False)
                    self.highest_streak = state_data.get('highest_streak', 0)
                print("State loaded successfully.")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading state: {e}. Starting fresh.")
                # Reset state if loading fails
                self._reset_state()
        else:
            print("No state file found. Starting fresh.")
            # Reset state if the file does not exist
            self._reset_state()

    def save(self):
        """
        Saves the current tracker state to the STATE_FILE in JSON format.
        Converts the last_check_in_date to a string for serialization.
        """
        # Convert the date object to a string for JSON serialization
        last_date_str = self.last_check_in_date.isoformat() if self.last_check_in_date else None
        state_data = {
            'streak_count': self.streak_count,
            'cheat_days': self.cheat_days,
            'last_check_in_date': last_date_str,
            'is_game_over': self.is_game_over,
            'highest_streak': self.highest_streak # Save the highest streak
        }
        try:
            with open(STATE_FILE, 'w') as f:
                # Use indent for readability in the JSON file
                json.dump(state_data, f, indent=4)
            print("State saved successfully.")
        except IOError as e:
            print(f"Error saving state: {e}")

    def check_in(self):
        """
        Handles the daily check-in logic. Determines if the streak continues,
        if a day was missed, if a cheat day is used, or if the game is over.
        Returns a message string indicating the outcome.
        """
        today = datetime.date.today()

        # If the game is over, prevent checking in and return a specific message
        if self.is_game_over:
            return "Game is Over. Click 'Start New Game' to begin again."

        # If the user has already checked in today, return a message
        if self.last_check_in_date == today:
            return "You have already checked in today."

        message = "" # Initialize the message string

        # Check if this is the very first check-in
        if self.last_check_in_date is None:
            self.streak_count = 1
            self.last_check_in_date = today
            message = "Welcome! Your first check-in recorded. Streak: 1 day."
        # Check if the user checked in on the consecutive day
        elif today == self.last_check_in_date + datetime.timedelta(days=1):
            # Streak continues: increment streak, update last check-in date
            self.streak_count += 1
            self.last_check_in_date = today
            message = f"Checked in! Streak continues: {self.streak_count} days."

            # Check if a cheat day is earned based on the streak rate
            if self.streak_count > 0 and self.streak_count % self.CHEAT_DAY_EARN_RATE == 0:
                 self.cheat_days += 1
                 message += f"\nEarned a cheat day! Total cheat days: {self.cheat_days}"

        # If today is not the day after the last check-in, a day was missed
        else:
            # Check if the user has cheat days available
            if self.cheat_days > 0:
                # Use a cheat day: decrement cheat days, reset streak
                self.cheat_days -= 1
                # Record the current streak as the highest before resetting
                self.highest_streak = max(self.highest_streak, self.streak_count)
                self.streak_count = 0 # Streak is broken, reset to 0
                self.last_check_in_date = today # Record today as the start of a new potential streak
                message = f"Missed a day! Used a cheat day. Streak reset to 0. Cheat days remaining: {self.cheat_days}."
            else:
                # No cheat days left: Game Over
                self.is_game_over = True
                # Record the current streak as the highest before game over
                self.highest_streak = max(self.highest_streak, self.streak_count)
                self.streak_count = 0 # Streak is 0 when game over occurs
                self.last_check_in_date = today # Record the day game over happened
                message = "GAME OVER! You missed a day with no cheat days left."

        # Check for milestone messages based on the current streak count
        milestone_message = self.MILESTONES.get(self.streak_count)
        if milestone_message:
            if isinstance(milestone_message, dict): # Handle potential image keys later
                 message += f"\nMilestone Achieved: {milestone_message.get('message', 'Milestone!')}"
                 # Logic to handle image display would be in the view/controller
            else:
                 message += f"\nMilestone Achieved: {milestone_message}"

        # Save the state after every check-in attempt
        self.save()

        # Return the final message
        return message

    def start_new_game(self):
        """
        Resets the tracker state to start a new game, preserving the highest streak record.
        """
        self.streak_count = 0
        self.cheat_days = 0
        self.last_check_in_date = None # Reset the last check-in date
        self.is_game_over = False
        # The highest_streak is intentionally preserved here

        # Save the reset state
        self.save()
        print("New game state saved.")

    # --- Testing Methods (TEMPORARY - ONLY FOR TESTING) ---
    # These methods are used by the automated test script to manipulate the state
    # for specific test scenarios. They should be removed for a production version.

    def set_last_check_in_date_for_testing(self, year, month, day):
        """Sets the last check-in date to a specific date for testing purposes."""
        try:
            self.last_check_in_date = datetime.date(year, month, day)
            print(f"--- Testing: Last check-in date set to {self.last_check_in_date} ---")
        except ValueError as e:
            print(f"--- Testing Error: Invalid date provided - {e} ---")
            # This error indicates a problem with the date provided in the test setup.

    def advance_date_for_testing(self, days):
        """Advances the last check-in date by a number of days for testing purposes."""
        if self.last_check_in_date:
            self.last_check_in_date += datetime.timedelta(days=days)
            print(f"--- Testing: Last check-in date advanced by {days} days to {self.last_check_in_date} ---")
        else:
            print("--- Testing: Cannot advance date, last check-in date is None ---")

    def _reset_state(self):
        """
        Helper method to reset the core state attributes to their initial values.
        Used internally and by the test script for clean test setups.
        """
        self.streak_count = 0
        self.cheat_days = 0
        self.last_check_in_date = None
        self.is_game_over = False
        self.highest_streak = 0
        # Note: This method does NOT save the state; the caller is responsible for saving.
    # --- End Testing Methods ---
