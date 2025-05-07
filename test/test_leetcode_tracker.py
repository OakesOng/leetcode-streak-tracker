import tkinter as tk
import sys
import os
import datetime

# Add the parent directory to the Python path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the necessary classes from your application
from tracker_model import TrackerState
from tracker_view import TrackerView # We still need TrackerView to instantiate Controller, but won't use its GUI methods
from tracker_controller import TrackerController

# --- Define Test Cases ---
# Each test case is a dictionary with:
# 'name': A descriptive name for the test.
# 'initial_state_setup': A function that takes model and controller and sets up the initial state.
# 'action': The method to call (e.g., controller.handle_check_in).
# 'expected_state': A dictionary of expected values for model attributes after the action.
# 'expected_message_part': A substring expected to be in the message returned by check_in.

def setup_streak_continuation(model, controller):
    """Sets up state for testing streak continuation."""
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    model.set_last_check_in_date_for_testing(yesterday.year, yesterday.month, yesterday.day)
    model.streak_count = 5 # Start with a sample streak
    model.cheat_days = 0
    model.is_game_over = False
    model.highest_streak = 5 # Set highest streak to match initial streak for this test

def setup_missed_day_game_over(model, controller):
    """Sets up state for testing missed day leading to game over."""
    two_days_ago = datetime.date.today() - datetime.timedelta(days=2)
    model.set_last_check_in_date_for_testing(two_days_ago.year, two_days_ago.month, two_days_ago.day)
    model.streak_count = 5 # Set a sample streak
    model.cheat_days = 0 # No cheat days
    model.is_game_over = False
    model.highest_streak = 5 # Set highest streak to match initial streak for this test

def setup_earn_cheat_day(model, controller):
    """Sets up state for testing earning a cheat day."""
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    model.set_last_check_in_date_for_testing(yesterday.year, yesterday.month, yesterday.day)
    model.streak_count = 13 # Streak just before earning a cheat day (if rate is 14)
    model.cheat_days = 0
    model.is_game_over = False
    model.highest_streak = 13 # Set highest streak

def setup_missed_day_with_cheat_day(model, controller):
    """Sets up state for testing missed day with a cheat day available."""
    two_days_ago = datetime.date.today() - datetime.timedelta(days=2)
    model.set_last_check_in_date_for_testing(two_days_ago.year, two_days_ago.month, two_days_ago.day)
    model.streak_count = 5 # Set a sample streak to show it resets
    model.cheat_days = 1 # Have a cheat day
    model.is_game_over = False
    model.highest_streak = 5 # Set highest streak

def setup_check_in_when_game_over(model, controller):
    """Sets up state for testing check-in when already game over."""
    # The date here doesn't strictly matter for this test, but let's set it
    today = datetime.date.today()
    model.set_last_check_in_date_for_testing(today.year, today.month, today.day)
    model.streak_count = 0
    model.cheat_days = 0
    model.is_game_over = True # Game is already over
    model.highest_streak = 55 # Sample highest streak from a previous game

TEST_CASES = [
    {
        'name': 'Test Case 1: Streak Continuation',
        'initial_state_setup': setup_streak_continuation,
        'action': 'check_in',
        'expected_state': {'streak_count': 6, 'cheat_days': 0, 'is_game_over': False, 'highest_streak': 5},
        'expected_message_part': "Streak continues: 6 days."
    },
    {
        'name': 'Test Case 2: Missed Day (Game Over)',
        'initial_state_setup': setup_missed_day_game_over,
        'action': 'check_in',
        'expected_state': {'streak_count': 0, 'cheat_days': 0, 'is_game_over': True, 'highest_streak': 5},
        'expected_message_part': "GAME OVER! You missed a day with no cheat days left."
    },
     {
        'name': 'Test Case 3: Earn Cheat Day',
        'initial_state_setup': setup_earn_cheat_day,
        'action': 'check_in',
        'expected_state': {'streak_count': 14, 'cheat_days': 1, 'is_game_over': False, 'highest_streak': 13},
        'expected_message_part': "Earned a cheat day! Total cheat days: 1"
    },
    {
        'name': 'Test Case 4: Missed Day with Cheat Day',
        'initial_state_setup': setup_missed_day_with_cheat_day,
        'action': 'check_in',
        'expected_state': {'streak_count': 0, 'cheat_days': 0, 'is_game_over': False, 'highest_streak': 5},
        'expected_message_part': "Missed a day! Used a cheat day." # Check for part of the message
    },
     {
        'name': 'Test Case 5: Check in when Game Over',
        'initial_state_setup': setup_check_in_when_game_over,
        'action': 'check_in',
        'expected_state': {'streak_count': 0, 'cheat_days': 0, 'is_game_over': True, 'highest_streak': 55}, # State should remain unchanged
        'expected_message_part': "Game is Over. Click 'Start New Game' to begin again."
    },
    # Add more test cases here following the same structure
]

# --- Test Runner ---
def run_tests():
    print("--- Running Automated Tests ---")
    all_tests_passed = True

    for i, test_case in enumerate(TEST_CASES):
        print(f"\nRunning {test_case['name']}...")

        # Create fresh instances for each test to avoid state leakage
        # We need a dummy Tkinter root and View for the Controller initialization,
        # but we won't run the mainloop or interact with the GUI.
        root = tk.Tk()
        root.withdraw() # Hide the main window
        model = TrackerState()
        view = TrackerView(root)
        controller = TrackerController(model, view)

        # IMPORTANT: Prevent the controller from loading the actual state file
        # for each test case. We want to control the initial state explicitly.
        # A simple way is to reset the state after controller init, or
        # modify TrackerState.load to have a test mode.
        # Let's explicitly reset to a known base state before setup.
        model._reset_state() # Use the internal reset method

        # 1. Set up initial state
        test_case['initial_state_setup'](model, controller)

        # 2. Perform the action (simulate button click)
        # We call the controller's handler directly
        if test_case['action'] == 'check_in':
            actual_message = controller.handle_check_in() # handle_check_in calls model.check_in and returns its message
        else:
            print(f"Error: Unknown action '{test_case['action']}' for {test_case['name']}")
            all_tests_passed = False
            root.destroy() # Clean up the dummy root
            break # Stop on error

        # 3. Verify the final state
        state_matches = True
        actual_state = {
            'streak_count': model.streak_count,
            'cheat_days': model.cheat_days,
            'is_game_over': model.is_game_over,
            'highest_streak': model.highest_streak,
            # We don't strictly test last_check_in_date here as it's dynamic (today)
        }

        for key, expected_value in test_case['expected_state'].items():
            if actual_state.get(key) != expected_value:
                print(f"  FAIL: State mismatch for {key}. Expected: {expected_value}, Got: {actual_state.get(key)}")
                state_matches = False
                all_tests_passed = False

        # 4. Verify the message
        message_matches = test_case['expected_message_part'] in actual_message
        if not message_matches:
            print(f"  FAIL: Message mismatch. Expected to contain: '{test_case['expected_message_part']}', Got: '{actual_message}'")
            all_tests_passed = False

        if state_matches and message_matches:
            print("  PASS")
        else:
            print("  FAIL")
            # Optional: Break on first failure
            # root.destroy() # Clean up the dummy root
            # sys.exit(1) # Exit with a non-zero status code

        root.destroy() # Clean up the dummy root after each test

    if all_tests_passed:
        print("\n--- All Automated Tests Passed! ---")
    else:
        print("\n--- Some Tests Failed ---")
        sys.exit(1) # Exit with a non-zero status code if any test failed

if __name__ == "__main__":
    run_tests()
