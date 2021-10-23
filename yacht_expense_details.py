import io
import json
from bidi.algorithm import get_display
from prompt_toolkit import print_formatted_text, HTML

import utils

_ = utils.load_translation()

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
    dict = {'remarks': remarks, 'category': category, 'store': store, 'is_boat_upgrade': upgrade}
    return str(dict)


def review_all_expenses(jsonfile):
    j = json.load(io.open(jsonfile, 'r', encoding='utf-8-sig'))
    j = j['expenses']
    for expense in j:
        if expense['deleted_at']:
            continue
        update_expense(expense)


def update_expense(expense):
    print('---------------------------------------------------------------------------------------')
    updated_expense = expense
    print_formatted_text(HTML('<ansigreen>' + _('Description: ') + '</ansigreen>' + get_display(
        expense['description']) + '(' + utils.to_simple_local_date_string(expense['date']) + ')'))
    ug = False
    category = ''
    if utils.is_json(expense['details']):
        det = json.loads(expense['details'])
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

    else:
        print_formatted_text(
            HTML('<ansigreen>' + _('Details: ') + '</ansigreen>' + get_display(str(expense['details']))))

        # print(_('Is considered upgrade?'))
        ug = utils.default_input(_('Is considered upgrade?') + '(Y/N)', 'N', ['Y', 'N'], ignore_case=True)
        category = utils.default_input(_('Expense category?'),'Other', options=categories,
                                       ignore_case=True)

    ug = utils.convert_yn_to_bool(ug)
    new_details = create_details_json(expense['details'], category, '', ug)
    print(new_details)

    return updated_expense
