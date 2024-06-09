import json
import os
from habit import Habit, Periodicity
from utils import generate_random_dates, generate_random_dates_per_week
from datetime import datetime
from typing import Union, Tuple

class HabitTracker:
    """
    A class to manage a list of habits.

    This class provides methods to create and manage a list of Habit objects. It also provides methods to 
    load and save the list of habits to a JSON file.

    Attributes:
        data (list[Habit]): A list of Habit objects.

    Methods:
        create_habit(): Create a new habit and add it to the data list.
    """
    def __init__(self) -> None:
        """
        Initialize a HabitTracker object.

        This method checks if a JSON file named "data.json" exists in the current directory. If it does, 
        it loads the list of habits from the file. If it doesn't, it creates a new file and initializes 
        an empty list of habits.
        """
        if "data.json" not in os.listdir():
            with open("data.json", "w") as file:
                json.dump([], file)
                self.data: list[Habit] = []
        else:
            with open("data.json", "r") as file:
                self.data = json.load(file)
                if type(self.data) == list:
                    self.data = [Habit.from_dict(habit) for habit in self.data]

    def create_habit(self):
        """
        Create a new habit and add it to the data list.

        This method prompts the user to enter the details of a new habit. If a habit with the same name 
        already exists, it prints a message saying that the habit already exists. Otherwise, it adds the 
        new habit to the data list.

        Raises:
            ValueError: If a habit with the same name already exists.
        """
        habit = Habit.create_habit_from_cli()
        if habit.name in [habit.name for habit in self.data]:
            print(f"Habit with name {habit.name} already exists")
            return
        print(f"\tYour habit '{habit.name}' has been created successfully")
        print("\tYou can now check off this habit")
        self.data.append(habit)

    def save_habit(self, habit: Habit):
        """
        Save a habit to the data list.

        This method takes a Habit object and adds it to the data list.

        Args:
            habit (Habit): The Habit object to add to the data list.
        """
        self.data.append(habit)

    def view_all_habits(self):
        """
        Print all habits in the data list.

        This method prints a list of all habits in the data list. Each habit is printed on a new line.
        """
        for i, habit in enumerate(self.data):
            print(f"\t{i+1}. {habit.name} (Periodicity: {habit.periodicity})")
            

    def update_habit(self):
        """
        Update a habit in the data list.

        This method prompts the user to enter the name of a habit to check off. It then finds the habit in the 
        data list and calls the check_off method on it.

        Raises:
            ValueError: If a habit with the entered name does not exist in the data list.
        """
        print("\tHabits that can be checked off:")
        for i, habit in enumerate(self.data):
            if habit.can_check_off():
                last_checked_off = len(habit.completion_dates) > 0 and habit.date(habit.completion_dates[-1]) or 'Never'
                print(f"\t{i+1}. {habit.name} (Periodicity: {habit.periodicity}) (Last checked off: {last_checked_off})")
        habit_name = input("\tEnter the name of the habit you want to check off: ")
        try:
            habit, index = self.find_habit_from_name(habit_name)
            if habit is None:
                return
            if habit.can_check_off():
                habit.check_off()
                self.data[index] = habit
                print(f"\tChecked off habit: {habit}")
            else:
                print("\tYou can't check off this habit yet")
        except ValueError as e:
            print(e)

    def save_data(self):
        """
        Save the data list to a JSON file.

        This method converts each habit in the data list to a dictionary and saves the list of dictionaries 
        to a JSON file named "data.json".
        """
        data = [habit.to_dict() for habit in self.data]
        with open("data.json", "w") as file:
            json.dump(data, file)
        

    def find_habit_from_name(self, name: str) -> Tuple[Habit, int] | Union[None, None]:
        """
        Find a habit in the data list by name.

        This method takes a name and returns the first habit in the data list with that name, along with its index. 
        If no habit with that name exists, it prints a message and returns None and None.

        Args:
            name (str): The name of the habit to find.

        Returns:
            Habit: The first habit in the data list with the given name, or None if no such habit exists.
            int: The index of the habit in the data list, or None if no such habit exists.
        """
        i = 0
        for habit in self.data:
            if habit.name == name:
                return habit, i
            i += 1
        print(f"No habit with name {name}")
        return None, None
        
    def __str__(self) -> str:
        """
        Return a string representation of the HabitTracker object.

        This method returns a string with each habit in the data list on a new line.

        Returns:
            str: A string representation of the HabitTracker object.
        """
        return "\n".join([str(habit) for habit in self.data])
    
    def generate_sample_data(self):
        """
        Generate sample data for the HabitTracker.

        This method generates 3 daily habits and 2 weekly habits with random completion dates between 
        1st Jan 2024 and 1st Feb 2024 for daily habits, and between 1st Jun 2023 and 1st Dec 2023 for weekly habits. 
        It then adds these habits to the data list.
        """
        self.data = []
        daily_habits = ["Excercise", "Code", "Gaming"]
        weekly_habits = ["Read A book", "Meditate"]
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 2, 1)

        # weeks example data for 6 months
        week_start_date = datetime(2023, 6, 1)
        week_end_date = datetime(2023, 12, 1)
        for habit in daily_habits:
            completion_dates = generate_random_dates(start_date, end_date, 15)
            data = {
                "name": habit,
                "periodicity": Periodicity.DAILY.value,
                "creation_date": start_date.isoformat(),
                "completion_dates": [date.isoformat() for date in completion_dates]
            }
            self.data.append(Habit.from_dict(data))

        for habit in weekly_habits:
            completion_dates = generate_random_dates_per_week(week_start_date, week_end_date)
            data = {
                "name": habit,
                "periodicity": Periodicity.WEEKLY.value,
                "creation_date": week_start_date.isoformat(),
                "completion_dates": [date.isoformat() for date in completion_dates]
            }
            self.data.append(Habit.from_dict(data))
        self.save_data()