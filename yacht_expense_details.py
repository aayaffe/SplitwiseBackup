import io
import json

from prompt_toolkit.history import FileHistory

import splitwise
from bidi.algorithm import get_display
from prompt_toolkit import print_formatted_text, HTML, PromptSession

import config
import utils
from splitwise import Expense

_ = utils.load_translation()
session = PromptSession(history=FileHistory('storePromptHistory.hist'))

categories = [
    'Electronic maintenance',
    'Plumbing',
    'Deck',
    'Sails',
    'Engine',
    'General maintenance',
    'Electricity',
    'Berth',
    'Dry dock',
    'House',
    'Registration',
    'Insurance',
    'Electronics',
    'Safety',
    'Fuel (domestic)',
    'Other'
]


def create_details_json(remarks, category, store, upgrade):
    ret = {'remarks': remarks, 'category': category, 'store': store, 'is_boat_upgrade': upgrade}
    return json.dumps(ret, ensure_ascii=False).encode('utf8')


def review_all_expenses(expenses):
    return [update_expense(e) for e in expenses]


def update_expense(expense):
    if expense.deleted_at:
        return expense
    if expense.payment:
        return expense
    try:
        ignore_old_details = config.ignore_old_remarks
    except Exception:
        ignore_old_details = False
    try:
        skip_completed = config.skip_completed
    except Exception:
        skip_completed = False

    s = splitwise.Splitwise(config.consumer_key, config.consumer_secret,
                            api_key=config.API_key)
    print('---------------------------------------------------------------------------------------')
    print_formatted_text(HTML('<ansigreen>' + _('Description: ') + '</ansigreen>' + get_display(
        expense.description) + '(' + utils.to_simple_local_date_string(expense.date) + ')'))
    if utils.is_json(expense.details):
        if skip_completed:
            return expense
        det = json.loads(expense.details)
        upgrade = det['is_boat_upgrade']
        if upgrade:
            upgrade = 'Y'
        else:
            upgrade = 'N'
        ug = utils.default_input(_('Is considered upgrade?') + '(' + upgrade + ')', upgrade, ['Y', 'N'],
                                 ignore_case=True)
        category = det['category']
        category = utils.default_input(_('Expense category?'), category, categories,
                                       ignore_case=True)
        store = det['store']
        store = utils.session_input(_('Store?'), session, store)
        remarks = det['remarks']

    else:
        print_formatted_text(
            HTML('<ansigreen>' + _('Details: ') + '</ansigreen>' + get_display(str(expense.details))))

        ug = utils.default_input(_('Is considered upgrade?') + '(Y/N)', 'N', ['Y', 'N'], ignore_case=True)
        category = utils.default_input(_('Expense category?'), 'Other', options=categories,
                                       ignore_case=True)
        store = utils.session_input(_('Store?'), session, '')
        remarks = "" if ignore_old_details else expense.details

    ug = utils.convert_yn_to_bool(ug)
    new_details = create_details_json(remarks, category, store, ug)
    e = Expense()
    e.id = expense.id
    e.setDetails(new_details)
    return s.updateExpense(e)
