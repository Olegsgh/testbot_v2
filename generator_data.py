import csv
import random

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

data = ["agbis_dor_id,agbis_contr_id,agbis_doc_date,kredit,sclad_id".split(",")]

dates = ["2018-01-01",
         "2018-01-07",
         "2018-01-14",
         "2018-01-21",
         "2018-01-28",
         "2018-02-04",
         "2018-02-11",
         "2018-02-18",
         "2018-02-25",
         "2018-03-04"]

my_list = []
fieldnames = data[0]
for x in range(1000):
    values = [str(x), str(random.randint(1,20)), dates[random.randint(0,9)],str(random.randint(1,7)*1000), str(random.randint(1,10))]
    inner_dict = dict(zip(fieldnames, values))
    my_list.append(inner_dict)

path = "big_test_data.csv"
csv_dict_writer(path, fieldnames, my_list)