# LeetCode Streak Tracker

A gamified desktop application to help you build and maintain a consistent LeetCode practice routine. Track your daily problem-solving streaks, earn cheat days, and celebrate milestones—all within a simple, fun interface.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

## Features

- **Daily Check-Ins**: Log your daily LeetCode practice with a single click.
- **Streak Tracking**: Visualize consecutive days of activity to keep you motivated.
- **Cheat Days**: Earn one cheat day for every 14-day streak, letting you skip a day without losing progress.
- **Milestones**: Receive celebratory messages when you hit key milestones (e.g., 7 days, 30 days, 100 days).
- **Game Over Mechanics**: Miss a day without available cheat days, and the game ends—challenge yourself to start fresh!
- **Progress Bar**: Monitor your progress toward a 30-day cycle in real time.
- **Persistent Storage**: All data is saved locally in a JSON file between sessions.
- **MVC Architecture**: Organized codebase with Model, View, and Controller for easy maintenance and extensibility.
- **Automated Tests**: Core logic is covered by unit tests to ensure reliability.

## Prerequisites

- **Platform**: Windows 11 (tested on Windows 11)
- **Python**: Version 3.9
- **Environment Manager**: [conda](https://docs.conda.io/) (or any virtual environment manager)

## Installation## Installation

```bash
# Clone the repository
git clone https://github.com/<username>/leetcode-streak-tracker.git
cd leetcode-streak-tracker

# Create and activate a conda environment
conda create -n leetcode-tracker python=3.9
conda activate leetcode-tracker

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python leetcode_tracker.py
```

Once launched, follow these steps to manage your LeetCode streak:

- **Daily Check-In**: Click **Check In Today** to record your practice for the current day.
- **Earning Cheat Days**: For every 14 consecutive days of check-ins, you earn **1 cheat day**. Cheat days allow you to skip a single day without breaking your streak.
- **Missing a Day**:

  - If you have at least one cheat day available, you can miss a check-in and the app will automatically consume a cheat day to preserve your streak.
  - If you have **0 cheat days** and you miss a day, the game ends on your next check-in.

- **Game Over & Reset**: After a game over, click **Start New Game** to reset your streak (your highest streak is preserved in the stats) and begin a new cycle.
- **Progress Bar**: Monitor your progress toward the next 30-day cycle in real time via the progress bar.

## Running Tests

Navigate to the `test` directory and run the test script:

```bash
cd test
python test_leetcode_tracker.py
```

## Project Structure## Project Structure

```
.
├── leetcode_tracker.py           # Entry point for the application
├── tracker_model.py              # Core logic and state management
├── tracker_view.py               # GUI implementation using Tkinter
├── tracker_controller.py         # Bridges model and view (event handling)
├── requirements.txt              # Python package dependencies
├── test
│   └── test_leetcode_tracker.py  # Unit tests for core functionality
└── README.md                     # Project documentation
```
