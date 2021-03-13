from splitwise import Splitwise
import config
import json
import utils

s = Splitwise(config.consumer_key, config.consumer_secret,
              api_key=config.API_key)
utils.create_folder('export')
expenses = s.getExpenses(group_id=config.group_id)
expenses_array = []
for expense in expenses:
    comments = s.getComments(expense.id)
    js = json.loads(
        json.dumps(expense.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))  # .encode('utf8')
    comments_array = []
    for comment in comments:
        comment_json = json.loads(json.dumps(comment.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
        commenter = json.loads(json.dumps(comment.user.__dict__, default=lambda o: '<not serializable>', ensure_ascii=False))
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
    if expense.receipt.original:
        utils.image_downloader([expense.receipt.original], 'export')
    print(js)
    expenses_array.append(js)

with open('export/expenses.json', 'w', encoding='utf-8') as outfile:
    json.dump(expenses_array, outfile, ensure_ascii=False, indent=4)


