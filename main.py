from habit import Habit
from habittracker import HabitTracker
from analytics import habits_analytics

def main():
    """
    Main function to run the Habit Tracker application.

    This function creates a HabitTracker object and loads sample data if the data list is empty. It then 
    displays a menu and prompts the user to choose an option. Depending on the user's choice, it calls 
    the appropriate method on the HabitTracker object or the habits_analytics function.
    """
    menu = """
\t-----Habit Tracker-----\t
\tWeclome to the Habit Tracker
\tLoaded With Some Pre-Defined Habits
\tPlease Choose an Option Below
\t1. Create a new habit
\t2. Check off a habit
\t3. View all habits
\t4. Analytics
\t5. Exit 
"""
    habit_tracker = HabitTracker()
    if habit_tracker.data == []:
        habit_tracker.generate_sample_data()
    while True:
        choice = int(input(menu))
        
        if choice == 1:
            habit_tracker.create_habit()
        elif choice == 2:
            habit_tracker.update_habit()
        elif choice == 3:
            habit_tracker.view_all_habits()
        elif choice == 4:
            habits_analytics(habit_tracker)
        elif choice == 5:
            habit_tracker.save_data()
            break

if __name__ == "__main__":
    main()