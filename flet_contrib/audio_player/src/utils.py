# request this only when you have done timedelta(milliseconds=...)
def format_timedelta_str_ms(timedelta_milliseconds_str: str):
    """
    Examples:
    format_timedelta_str("0:00:40.399000") -> "00:40"
    format_timedelta_str("0:00:40.600000") -> "00:41"
    """
    time_ = timedelta_milliseconds_str.split(":")  # the whole split string
    seconds_field = time_[-1]
    seconds = seconds_field.split(".")[0]  # situation: 0:03:40.something
    try:
        microseconds = seconds_field.split(".")[1]  # if it exists
    except:
        pass  # if the microseconds field doesn't exist
    else:
        # basically, this is the process of rounding
        # first, convert the parts into numbers
        # process
        # round the output and convert into string
        time_[-1] = str(round(float(eval(seconds + "." + microseconds))))

    # the hours place
    if len(time_[0]) == 1 and time_[0] == "0":
        del time_[0]

    return ":".join(time_)
