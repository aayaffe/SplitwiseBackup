import json
from splitwise import Splitwise
import config
import utils
from excel import generate_expenses_xlsx
import yacht_expense_details

s = Splitwise(config.consumer_key, config.consumer_secret,
              api_key=config.API_key)
utils.create_folder(config.json_filename)
expenses = s.getExpenses(group_id=config.group_id, limit=config.expenses_list_limit)
group = s.getGroup(id=config.group_id)
members_json = group.__dict__['members']
members_array = json.loads(
        json.dumps(members_json, default=lambda o: o.__dict__, ensure_ascii=False))


def expenses_to_json(expenses):
    expenses_array = []
    for expense in expenses:
        comments = s.getComments(expense.id)
        js = json.loads(
            json.dumps(expense.__dict__, default=lambda o: o.__dict__, ensure_ascii=False))
        js['comments'] = json.loads(
                json.dumps(comments, default=lambda o: o.__dict__, ensure_ascii=False))
        if expense.receipt.original and config.download_images_pdf:
            utils.image_downloader([expense.receipt.original], config.receipts_dir, overwrite=False)
        print(js)
        expenses_array.append(js)
    json_out = {'expenses': expenses_array, 'members': members_array}
    with open(config.json_filename, 'w', encoding='utf-8') as outfile:
        json.dump(json_out, outfile, ensure_ascii=False, indent=4)


expenses_to_json(expenses)
generate_expenses_xlsx(config.xlsx_filename, config.json_filename)
yacht_expense_details.review_all_expenses(expenses)

# json2csv(config.json_filename, 'export/out.csv')
