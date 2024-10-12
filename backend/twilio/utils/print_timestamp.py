import datetime


def print_with_timestamp(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:23]
    print(f"{current_time} {message}")