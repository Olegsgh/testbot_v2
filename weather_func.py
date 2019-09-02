import csv

def get_weather_by_date(date):
    weather_w = "-1"
    with open("weather.csv") as w_obj:
        reader_w = csv.DictReader(w_obj, delimiter=';')
        for line_w in reader_w:
            if (line_w["date"] == date):
                weather_w = line_w['temp']
    return weather_w