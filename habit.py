from enum import Enum
from datetime import datetime

class Periodicity(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")

class Habit:
    """
    A class to represent a habit.

    Attributes:
        name (str): The name of the habit.
        periodicity (Periodicity.value): The periodicity of the habit, either 'daily' or 'weekly'.
        creation_date (datetime): The date and time when the habit was created.
        completion_dates (list[datetime]): A list of dates and times when the habit was completed.

    Methods:
        from_dict(data: dict): Create a Habit object from a dictionary.
        to_dict(): Convert the Habit object to a dictionary.
    """
    def __init__(self, name: str, periodicity: Periodicity) -> None:
        """
        Initialize a Habit object with a name, periodicity, creation date, and an empty list of completion dates.

        Args:
            name (str): The name of the habit.
            periodicity (Periodicity): The periodicity of the habit, either 'daily' or 'weekly'.
        """
        self.name: str = name
        self.periodicity: Periodicity.value = periodicity.value
        self.creation_date: datetime = datetime.now()
        self.completion_dates : list[datetime] = []
        
    @classmethod
    def from_dict(cls, data: dict) -> "Habit":
        """
        Create a Habit object from a dictionary.

        Args:
            data (dict): A dictionary with keys 'name', 'periodicity', 'creation_date', and 'completion_dates'.

        Returns:
            Habit: A Habit object with the data from the dictionary.
        """
        habit = cls(data["name"], Periodicity(data["periodicity"]))
        habit.creation_date = datetime.fromisoformat(data["creation_date"])
        habit.completion_dates = [datetime.fromisoformat(date) for date in data["completion_dates"]]
        return habit
    
    def to_dict(self) -> dict:
        """
        Convert the Habit object to a dictionary.

        Returns:
            dict: A dictionary with keys 'name', 'periodicity', 'creation_date', and 'completion_dates'.
        """
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date.isoformat(),
            "completion_dates": [date.isoformat() for date in self.completion_dates]
        }
    
    def check_off(self) -> None:
        """
        Mark the habit as completed for the current period.

        This method checks the last completion date of the habit and the current date. If the habit has not been 
        completed in the current period (day, week, month, or year, depending on the habit's periodicity), 
        it adds the current date and time to the list of completion dates.
        """
        if len(self.completion_dates) == 0:
            self.completion_dates.append(datetime.now())
        else:
            last_date = self.completion_dates[-1]
            if self.periodicity == Periodicity.DAILY:
                if last_date.date() != datetime.now().date():
                    self.completion_dates.append(datetime.now())
            elif self.periodicity == Periodicity.WEEKLY:
                if (datetime.now() - last_date).days >= 7:
                    self.completion_dates.append(datetime.now())

    @classmethod
    def create_habit_from_cli(cls):
        """
        Create a Habit object from user input in the command line interface.

        This method prompts the user to enter the name and periodicity of the habit. It then creates and returns a 
        new Habit object with these values.

        Returns:
            Habit: A new Habit object with the name and periodicity entered by the user.

        Raises:
            ValueError: If the user enters an invalid periodicity.
        """
        name = input("\tEnter the name of the habit: ")
        periodicity = input("\tEnter the periodicity of the habit (daily, weekly): ")
        if periodicity.upper() not in Periodicity.__members__:
            raise ValueError("Invalid periodicity")
        return cls(name, Periodicity(periodicity))

    
    def date(self, date: datetime) -> str:
        """
        Format a datetime object into a string.

        This method takes a datetime object and returns a string in the format "day month year at hour:minute am/pm".

        Args:
            date (datetime): The datetime object to format.

        Returns:
            str: A string representing the date and time in the format "day month year at hour:minute am/pm".
        """
        year, month, day = date.year, date.month, date.day
        am_pm = "pm" if date.time().hour >= 12 else "am"
        hour = date.time().hour - 12 if date.time().hour > 12 else date.time().hour
        minutes = date.time().minute

        return f"{day} {MONTHS[month-1]} {year} at {hour}:{minutes} {am_pm}"
    
    
    def can_check_off(self):
        """
        Determine if the habit can be checked off for the current period.

        This method checks the last completion date of the habit and the current date. If the habit has not been 
        completed in the current period (day or week, depending on the habit's periodicity), it returns True. 
        Otherwise, it returns False.

        Returns:
            bool: True if the habit can be checked off for the current period, False otherwise.

        Raises:
            ValueError: If the habit's periodicity is not 'daily' or 'weekly'.
        """
        if len(self.completion_dates) == 0:
            return True
        last_date = self.completion_dates[-1]
        if self.periodicity == Periodicity.DAILY:
            return last_date.date() != datetime.now().date()
        elif self.periodicity == Periodicity.WEEKLY:
            return (datetime.now() - last_date).days >= 7
        elif self.periodicity == Periodicity.MONTHLY:
            return last_date.month != datetime.now().month
        elif self.periodicity == Periodicity.YEARLY:
            return last_date.year != datetime.now().year

    def __str__(self) -> str:
        """
        Return a string representation of the Habit object.

        This method returns a string in the format "Habit(name=name, periodicity=periodicity)", 
        where name and periodicity are the name and periodicity of the habit.

        Returns:
            str: A string representation of the Habit object.
        """
        return f"Habit(name={self.name}, periodicity={self.periodicity})"
    
    def __repr__(self) -> str:
        """
        Return a string representation of the Habit object.

        This method calls the __str__ method to get a string representation of the Habit object.

        Returns:
            str: A string representation of the Habit object.
        """
        return str(self.__str__())


