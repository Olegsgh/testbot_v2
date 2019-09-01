import os
import re
import csv
import generator_data

from datetime import datetime
from pymongo import MongoClient

MONGODB_URI = os.environ['MONGODB_URI']

mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client.get_default_database()
mongo_logs = mongo_db.get_collection('logs')

def get_previous_date(date):
    index = generator_data.dates.index(date)
    if index >= 1:
        return generator_data.dates[index-1]
    else:
        return "-1"


def get_date(message):
    return re.findall(r'\d{4}-\d{2}-\d{2}', message)[0]

def reply_full_week_report(message):
    date = get_date(message.text)
    previous_date = get_previous_date(date)
    weather_w = 0
    response = ""
    with open("big_test_data.csv") as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')
        count_row = 0
        count_kredit = 0
        count_row_per = 0
        count_kredit_per = 0
        for line in reader:
            if (line["agbis_doc_date"] == date):
                count_row += 1
                try:
                    kredit = int(line['kredit'])
                    count_kredit += kredit
                except Exception as e:
                    print('not a number')
            if (line["agbis_doc_date"] == previous_date):
                count_row_per += 1
                try:
                    kredit = int(line['kredit'])
                    count_kredit_per += kredit
                except Exception as e:
                    print('not a number')
        response = "За дату " + date + " было " + "\n" + str(count_row) + " покупок " + "\n" + "на сумму " + str(count_kredit)
        if (previous_date != "-1"):
            response += "\n "
            response += "\n"
            response += "За предыдущую дату " + previous_date + " было " + "\n" + str(count_row_per) + " покупок " + "\n" + "на сумму " + str(
            count_kredit_per)
            response += "\n"
            response += "\n"
            if (count_row - count_row_per > 0):
                response += "Прирост по количеству составил " + str(round((count_row/count_row_per - 1)*100)) + "% \U0001F601"
                response += "\n"
            else:
                response += "Убыль по количеству составила " + str(round((count_row_per / count_row - 1)*100)) + "% \U0001F614"
                response += "\n"
            if (count_kredit - count_kredit_per > 0):
                response += "Прирост по сумме составил " + str(round((count_kredit/count_kredit_per - 1)*100)) + "% \U0001F601"
            else:
                response += "Убыль по сумме составила " + str(round((count_kredit_per / count_kredit - 1)*100)) + "% \U0001F614"
                response += "Убыль по сумме составила " + str(round((count_kredit_per / count_kredit - 1)*100)) + "%"

        with open("weather.csv") as w_obj:
            reader_w = csv.DictReader(w_obj, delimiter=';')
            for line in reader_w:
                if (line["date"] == date):
                    weather_w = int(line['temp'])
        response += weather_w
        mongo_logs.insert_one({
            "text": message.text,
            "response": response,
            "user_nickname": message.from_user.username,
            "timestamp": datetime.utcnow()
        })
        return response

def reply_kredit_week_report(message):
    date = get_date(message.text)
    response = ""
    with open("big_test_data.csv") as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')
        count_kredit = 0
        for line in reader:
            if (line["agbis_doc_date"] == date):
                try:
                    kredit = int(line['kredit'])
                    count_kredit += kredit
                except Exception as e:
                    print('not a number')
        response = response + "За дату " + date + " было покупок на сумму " + "\n " + str(count_kredit)
        mongo_logs.insert_one({
            "text": message.text,
            "response": response,
            "user_nickname": message.from_user.username,
            "timestamp": datetime.utcnow()
        })
        return response



def reply_count_week_report(message):
    date = get_date(message.text)
    response = ""
    with open("big_test_data.csv") as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')
        count_row = 0
        for line in reader:
            if (line["agbis_doc_date"] == date):
                count_row += 1

        response = response + "За дату " + date + " было " + "\n " + str(count_row) + " покупок"
        mongo_logs.insert_one({
            "text": message.text,
            "response": response,
            "user_nickname": message.from_user.username,
            "timestamp": datetime.utcnow()
        })
        return response



def reply_with_log(message, response):
    response = response + " - вот херь"
    mongo_logs.insert_one({
        "text": message.text,
        "response": response,
        "user_nickname": message.from_user.username,
        "timestamp": datetime.utcnow()
    })
    return response

def get_old_message():
    messages_list = list(mongo_logs.find())
    result = '<div>There are {} messages total. The last 10 are: </div><table>'.format(len(messages_list))
    row_template = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
    result += row_template.format('time', 'user', 'text from user', 'response from bot')
    for message in messages_list[-10:]:
        result += row_template.format(
            message['timestamp'], message['user_nickname'], message['text'], message['response']
        )
    result += '</table>'
    return result