from habit import Habit
from datetime import datetime
from habittracker import HabitTracker

def get_habit_streaks(habit: Habit):
    """
    Calculate and return the shortest, average, and longest streaks of a habit.

    A streak is defined as a continuous period of time where the habit is completed daily or weekly,
    depending on the habit's periodicity. The start of a streak is the day the habit is registered.

    Args:
        habit (Habit): The habit object containing the completion dates and periodicity.

    Returns:
        tuple: A tuple containing the shortest, average, and longest streaks, and a list of all streaks.
        The average streak is rounded to the nearest whole number.

    Raises:
        ValueError: If the habit's periodicity is not 'daily' or 'weekly'.
    """
    completion_dates = sorted(habit.completion_dates)
    if len(completion_dates) == 0:
        return 0, 0, 0, []
    if len(completion_dates) == 1:
        return 1, 1, 1, [1]
    streaks = []
    streak = 1
    if habit.periodicity == 'daily':
        for i in range(1, len(completion_dates)):
            if (completion_dates[i].date() - completion_dates[i-1].date()).days == 1:
                streak += 1
            else:
                streaks.append(streak)
                streak = 1
    elif habit.periodicity == 'weekly':
        for i in range(1, len(completion_dates)):
            if (completion_dates[i].date() - completion_dates[i-1].date()).days <= 7:
                streak += 1
            else:
                streaks.append(streak)
                streak = 1
    else:
        raise ValueError("Invalid periodicity")
    return min(streaks), round(sum(streaks)/len(streaks)), max(streaks), streaks

def get_longest_habit_streak(habits: list[Habit]):
    """
    Calculate and return the habit with the longest streak from a list of habits.

    This function iterates over the provided list of habits, calculates the longest streak for each habit,
    and then returns the name of the habit with the longest streak.

    Args:
        habits (list[Habit]): A list of Habit objects to analyze.

    Returns:
        str: The name of the habit with the longest streak.

    Raises:
        ValueError: If the habits list is empty.
    """
    longest_streaks = {}
    if not habits or len(habits) == 0:
        raise ValueError("No habits provided")
    for habit in habits:
        longest_streaks[habit.name] = (get_habit_streaks(habit)[2])
    return max(longest_streaks, key=longest_streaks.get)

def get_habits_with_same_periodicity(habits: list[Habit], periodicity: str):
    """
    Filter and return habits from a list that have the same periodicity.

    This function iterates over the provided list of habits and returns a new list containing only 
    the habits that have the same periodicity as the provided periodicity.

    Args:
        habits (list[Habit]): A list of Habit objects to filter.
        periodicity (str): The periodicity to filter by. This should be 'daily' or 'weekly'.

    Returns:
        list[Habit]: A list of Habit objects that have the same periodicity as the provided periodicity.

    Raises:
        ValueError: If the habits list is empty or if the periodicity is not 'daily' or 'weekly'.
    """
    if not habits or len(habits) == 0:
        raise ValueError("No habits provided")
    return [habit for habit in habits if habit.periodicity == periodicity]

def habits_analytics(tracker: HabitTracker):
    """
    Provide an interactive menu for analyzing habits.

    This function displays a menu with options to analyze habits in various ways, including:
    - Getting the shortest, average, and longest streaks of a habit
    - Getting the habit with the longest streak
    - Getting all habits with the same periodicity

    The function loops indefinitely until the user chooses to go back to the main menu.

    Args:
        tracker (HabitTracker): The HabitTracker object containing the habits to analyze.
    """
    menu = """
    \t-----Analytics-----\t
    \tPlease Choose an Option Below
    \t1. Get the shortest, average, and longest streaks of a habit
    \t2. Get the habit with the longest streak
    \t3. Get all habits with the same periodicity
    \t4. Go Back To Main Menu
    """
    while True:
        choice = int(input(menu))
        if choice == 1:
            habit_name = input("\tEnter the name of the habit: ")
            if tracker.find_habit_from_name(habit_name) is None:
                print("Habit not found")
                continue
            habit = tracker.find_habit_from_name(habit_name)[0]
            shortest, average, longest, streaks = get_habit_streaks(habit)
            print(f"\tShortest Streak: {shortest}")
            print(f"\tAverage Streak: {average}")
            print(f"\tLongest Streak: {longest}")
        if choice == 2:
            print(f"The habit with the longest streak is: '{get_longest_habit_streak(tracker.data)}'")
        if choice == 3:
            periodicity = input("\tEnter the periodicity (daily, weekly) : ")
            if periodicity not in ['daily', 'weekly']:
                print("\tInvalid periodicity")
                continue
            habits = get_habits_with_same_periodicity(tracker.data, periodicity)
            for index, habit in enumerate(habits):
                print(f"{index + 1}. {habit.name}")

        if choice == 4:
            break