from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_random_dates(start_date: datetime, end_date: datetime, n: int) -> list[datetime]:
    """
    Generate n random dates between start_date and end_date.

    This method generates n unique random dates between start_date and end_date.

    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.
        n (int): The number of dates to generate.

    Returns:
        list[datetime]: A list of n unique random dates between start_date and end_date.
    """
    fake_dates = []
    while True:
        fake_date = fake.date_between(start_date=start_date, end_date=end_date)
        fake_dates.count(fake_date) == 0 and fake_dates.append(fake_date)
        if len(fake_dates) == n:
            break

    fake_dates.sort()
    return fake_dates
    
    
def generate_random_dates_per_week(start_date: datetime, end_date: datetime) -> list[datetime]:
    """
    Generate random dates between start_date and end_date, with only one date per week.

    This method generates unique random dates between start_date and end_date, with a maximum of one date per week.

    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.

    Returns:
        list[datetime]: A list of unique random dates between start_date and end_date, with a maximum of one date per week.
    """
    dates = []
    weeks = set()

    while start_date <= end_date:
        date = fake.date_between(start_date=start_date, end_date=end_date)
        week_number = date.isocalendar()[1]

        if week_number not in weeks:
            dates.append(date)
            weeks.add(week_number)

        start_date += timedelta(days=7)

    dates.sort()
    return dates