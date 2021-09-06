import json
from splitwise import Splitwise
import config
import utils
from excel import generate_expenses_xlsx


s = Splitwise(config.consumer_key, config.consumer_secret,
              api_key=config.API_key)
utils.create_folder(config.json_filename)
expenses = s.getExpenses(group_id=config.group_id, limit=config.expenses_list_limit)
group = s.getGroup(id=config.group_id)
members_json = group.__dict__['members']
members_array = []
for member in members_json:
    js = json.loads(
        json.dumps(member.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))  # .encode('utf8')
    js['balance'] = json.loads(
        json.dumps(member.balances, default=lambda o: '<not serializable>', ensure_ascii=False))  # .encode('utf8')
    members_array.append(js)

expenses_array = []
for expense in expenses:
    comments = s.getComments(expense.id)
    js = json.loads(
        json.dumps(expense.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
    comments_array = []
    for comment in comments:
        comment_json = json.loads(
            json.dumps(comment.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
        commenter = json.loads(
            json.dumps(comment.user.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
        comment_json['user'] = commenter
        comments_array.append(comment_json)
    repayments_array = []
    for repayment in expense.repayments:
        repayment_json = json.loads(
            json.dumps(repayment.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
        repayments_array.append(repayment_json)

    users_array = []
    for user in expense.users:
        users_array.append(
            json.loads(json.dumps(user.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False)))
    js['comments'] = comments_array
    js['repayments'] = repayments_array

    js['users'] = users_array
    if expense.created_by:
        js['created_by'] = json.loads(
            json.dumps(expense.created_by.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
    if expense.updated_by:
        js['updated_by'] = json.loads(
            json.dumps(expense.updated_by.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
    if expense.deleted_by:
        js['deleted_by'] = json.loads(
            json.dumps(expense.deleted_by.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
    js['receipt'] = json.loads(
        json.dumps(expense.receipt.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
    js['category'] = json.loads(
        json.dumps(expense.category.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
    if expense.receipt.original and config.download_images_pdf:

        utils.image_downloader([expense.receipt.original], config.receipts_dir)
    print(js)
    expenses_array.append(js)
json_out = {'expenses': expenses_array, 'members': members_array}
with open(config.json_filename, 'w', encoding='utf-8') as outfile:
    json.dump(json_out, outfile, ensure_ascii=False, indent=4)

generate_expenses_xlsx(config.xlsx_filename, config.json_filename)

# json2csv(config.json_filename, 'export/out.csv')
