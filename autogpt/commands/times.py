from datetime import datetime


def get_datetime() -> str:
    """Return the current date and time

    Returns:
        str: The current date and time
    """
    # return "Current date and time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "当前的日期和时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
