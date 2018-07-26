from datetime import date, datetime

def day_check(release):
    ptime = datetime.strptime( release, "%Y-%m-%dT%H:%M:%S.%fZ" )

    release_time = date(ptime.year,ptime.month,ptime.day)
    current_time = date(datetime.today().year,datetime.today().month,datetime.today().day)

    diff = current_time - release_time
    return diff.days

