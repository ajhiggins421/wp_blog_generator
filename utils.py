import radar


def random_date(date_bound):
    return str(radar.random_datetime(start=date_bound[0], stop=date_bound[1])).replace(" ", "T")


def random_time(date_bound):
    return str(radar.random_datetime(start=date_bound[0], stop=date_bound[1])).split(" ")[1]
