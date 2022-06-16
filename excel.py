import io
import json
from _datetime import datetime
from xlsxwriter.utility import xl_rowcol_to_cell

import config
import utils
from utils import create_folder
import xlsxwriter
import dateutil.parser
import gettext

el = gettext.translation('excel', localedir='locales', languages=[config.language])
el.install()
_ = el.gettext


def json2dict(jsonfile):
    j = json.load(io.open(jsonfile, 'r', encoding='utf-8-sig'))
    ret = {}
    users = {x['id']: x['first_name'] for x in j['members']}
    for expense in j['expenses']:
        if expense['deleted_at']:
            continue
        i = expense['id']
        ret[i] = {}
        ret[i]['date'] = utils.to_simple_local_date_string(expense['date'])
        ret[i]['description'] = expense['description']
        ret[i]['cost'] = -1 * float(expense['cost']) if expense['creation_method'] == 'reimbursement' else float(expense['cost'])
        ret[i]['details'] = expense['details']
        ret[i]['receipt'] = expense['receipt']['original']
        users_dict = {}
        for ID, name in users.items():
            users_dict[ID] = {}
            users_dict[ID]['first_name'] = name
            users_dict[ID]['paid_share'] = 0
            users_dict[ID]['owed_share'] = 0
        for user in expense['users']:
            users_dict[user['id']]['first_name'] = user['first_name']
            users_dict[user['id']]['paid_share'] = user['paid_share']
            users_dict[user['id']]['owed_share'] = user['owed_share']
        ret[i]['users'] = users_dict
    return ret


def json2usersdict(jsonfile):
    j = json.load(io.open(jsonfile, 'r', encoding='utf-8-sig'))
    ret = {x['id']: x['first_name'] for x in j['members']}
    return ret


def add_debt_ConditionalFormat(worksheet, cell, c_format):
    worksheet.conditional_format(cell, {'type': 'cell',
                                        'criteria': '>=',
                                        'value': 0,
                                        'format': c_format})


def add_owed_ConditionalFormat(worksheet, cell, c_format):
    worksheet.conditional_format(cell, {'type': 'cell',
                                        'criteria': '<',
                                        'value': 0,
                                        'format': c_format})


def generate_expenses_xlsx(filename, jsonfile):
    create_folder(filename)
    workbook = xlsxwriter.Workbook(filename)
    worksheet_name = _('Expenses ')
    worksheet = workbook.add_worksheet(worksheet_name)
    cell_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter'})
    url_cell_format = workbook.add_format({
        'border': 1,
        'valign': 'vcenter',
        'underline': 1,
        'font_color': 'blue'})
    bold_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'valign': 'vcenter'})
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'})
    currency_format = workbook.add_format({
        'num_format': '₪#,##0.0',
        'border': 1,
        'valign': 'vcenter'
    })
    currency_format_bold_minus = workbook.add_format({
        'num_format': '₪#,##0.0',
        'border': 1,
        'valign': 'vcenter',
        'bold': 1,
        'bg_color': '#FFC7CE',
        'font_color': '#9C0006'
    })
    currency_format_bold_plus = workbook.add_format({
        'num_format': '₪#,##0.0',
        'border': 1,
        'valign': 'vcenter',
        'bold': 1,
        'bg_color': '#C6EFCE',
        'font_color': '#006100'
    })

    user_dict = json2usersdict(jsonfile)
    first_user_column = 5
    cur_row = 0
    worksheet.merge_range(cur_row, 0, cur_row, first_user_column - 1 + len(user_dict) * 2,
                          worksheet_name + datetime.now().strftime(_("%d/%m/%Y")), merge_format)
    expense_dict = json2dict(jsonfile)

    cur_row += 1
    for i, user in enumerate(user_dict):
        worksheet.merge_range(cur_row, first_user_column + i * 2, cur_row, first_user_column+1 + i * 2, user_dict[user], merge_format)
        worksheet.write(cur_row + 1, first_user_column + i * 2, _('Paid'), bold_format)
        worksheet.write(cur_row + 1, first_user_column + 1 + i * 2, _('Owed'), bold_format)
    worksheet.merge_range(cur_row, 0, cur_row + 1, 0, _('Date'), merge_format)
    worksheet.merge_range(cur_row, 1, cur_row + 1, 1, _('Description'), merge_format)
    worksheet.merge_range(cur_row, 2, cur_row + 1, 2, _('Upgrade?'), merge_format)
    worksheet.merge_range(cur_row, 3, cur_row + 1, 3, _('Receipt'), merge_format)
    worksheet.merge_range(cur_row, 4, cur_row + 1, 4, _('Amount'), merge_format)

    cur_row += 1
    for expense in expense_dict:
        cur_row += 1
        worksheet.write(cur_row, 0, expense_dict[expense]['date'], bold_format)
        worksheet.write(cur_row, 1, expense_dict[expense]['description'], cell_format)
        try:
            details = json.loads(expense_dict[expense]['details'])
            upgrade = _('Yes') if bool(details['is_boat_upgrade']) else _('No')
        except Exception:
            upgrade = _('No')
        worksheet.write(cur_row, 2, upgrade, cell_format)
        link = expense_dict[expense]['receipt'] if expense_dict[expense]['receipt'] else ''
        if link:
            link = "receipts\\" + link.split("/")[-1:][0]
            worksheet.write_url(cur_row, 3, link, string=_('Yes') if expense_dict[expense]['receipt'] else _('No'),
                                cell_format=url_cell_format)
        else:
            worksheet.write(cur_row, 3, _('Yes') if expense_dict[expense]['receipt'] else _('No'), cell_format)
        worksheet.write_number(cur_row, 4, float(expense_dict[expense]['cost']), currency_format)

        for i, user in enumerate(expense_dict[expense]['users']):
            values = expense_dict[expense]['users'][user]
            worksheet.write_number(cur_row, first_user_column + i * 2, float(values['paid_share']), currency_format)
            worksheet.write_number(cur_row, first_user_column + i * 2 + 1, float(values['owed_share']), currency_format)

    cur_row += 1

    for i, user in enumerate(user_dict):
        topcell1 = xl_rowcol_to_cell(3, first_user_column + i * 2)
        bottomcell1 = xl_rowcol_to_cell(cur_row - 1, first_user_column + i * 2)
        topcell2 = xl_rowcol_to_cell(3, first_user_column+1 + i * 2)
        bottomcell2 = xl_rowcol_to_cell(cur_row - 1, first_user_column+1 + i * 2)
        bottomcell3 = xl_rowcol_to_cell(cur_row, first_user_column + i * 2)
        bottomcell4 = xl_rowcol_to_cell(cur_row, first_user_column+1 + i * 2)
        worksheet.write_formula(cur_row, first_user_column + i * 2, '=SUM(' + topcell1 + ':' + bottomcell1 + ')', currency_format)
        worksheet.write_formula(cur_row, first_user_column+1 + i * 2, '=SUM(' + topcell2 + ':' + bottomcell2 + ')', currency_format)
        worksheet.write_formula(cur_row + 1, first_user_column+1 + i * 2, '=' + bottomcell4 + ' - ' + bottomcell3, currency_format)
        add_owed_ConditionalFormat(worksheet, xl_rowcol_to_cell(cur_row + 1, first_user_column+1 + i * 2), currency_format_bold_plus)
        add_debt_ConditionalFormat(worksheet, xl_rowcol_to_cell(cur_row + 1, first_user_column+1 + i * 2), currency_format_bold_minus)

    worksheet.write_formula(cur_row, 4,
                            '=SUM(' + xl_rowcol_to_cell(3, 4) + ':' + xl_rowcol_to_cell(cur_row - 1, 4) + ')',
                            currency_format)
    worksheet.merge_range(cur_row, 0, cur_row, 2, _('Sum'), merge_format)
    worksheet.merge_range(cur_row + 1, 0, cur_row + 1, 2, _('Bottom line: Debt(+)/Owed(-)'), merge_format)

    worksheet.set_column(0, 0, 10)
    worksheet.set_column(1, 1, 50)
    worksheet.set_column(3, first_user_column - 1 + len(user_dict) * 2, 10)

    worksheet.set_landscape()
    worksheet.set_paper(9)
    # worksheet.print_area(0, 0, len(boat_rows), len(course_types) * (len(wind_speeds) + 2) - 2)
    worksheet.fit_to_pages(1, 1)
    if config.language == 'he':
        worksheet.right_to_left()
    workbook.close()
