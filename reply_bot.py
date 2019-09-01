import os
import re
import csv

from datetime import datetime
from pymongo import MongoClient

MONGODB_URI = os.environ['MONGODB_URI']

mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client.get_default_database()
mongo_logs = mongo_db.get_collection('logs')

def get_date(message):
    return re.findall(r'\d{4}-\d{2}-\d{2}', message)[0]

def reply_full_week_report(message):
    date = get_date(message.text)
    reader = csv.DictReader("test_data.csv", delimiter=',')
    count_row = 0
    count_kredit = 0
    for line in reader:
        if (line["agbis_doc_date"] == date):
            count_row += 1
            count_kredit += count_kredit
    return "За дату " + date + " было " + count_row + " покупок на сумму " + count_kredit

def reply_kredit_week_report(message):
    date = get_date(message.text)
    reader = csv.DictReader("test_data.csv", delimiter=',')
    count_kredit = 0
    for line in reader:
        if (line["agbis_doc_date"] == date):
            count_kredit += count_kredit
    return "За дату " + date + " было покупок на сумму " + count_kredit

def reply_count_week_report(message):
    date = get_date(message.text)
    reader = csv.DictReader("test_data.csv", delimiter=',')
    count_row = 0
    for line in reader:
        if (line["agbis_doc_date"] == date):
            count_row += 1
    return "За дату " + date + " было " + count_row + " покупок"



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