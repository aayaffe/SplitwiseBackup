import csv
import io
import json


def json2csv(jsonfile, csvfile):
    j = json.load(io.open(jsonfile, 'r', encoding='utf-8-sig'))
    with open(csvfile, 'w', newline='', encoding='utf-8-sig') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for e in j:
            users_arr = []
            for user in e['users']:
                users_arr.append(user['first_name'])
                users_arr.append(user['paid_share'])
                users_arr.append(user['owed_share'])
            csv_writer.writerow([e['date'], '"' + e['description'] + '"', e['cost']] + users_arr)