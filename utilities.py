
def generate_random_date():
    import random
    import datetime

    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2023, 3, 19)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    dt = datetime.datetime.strftime(random_date, "%d-%m-%Y | %H:%M:%S")
    return dt
