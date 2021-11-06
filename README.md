# SplitWiseExporter

SplitWiseExporter is a Python script used for backing up and exporting SplitWise group expenses.
It backs up all the expenses and receipts and generates a json file and optional XLSX or CSV file.

Work In Progress!

## Installation

Install requirements:
```bash
pip install -r requirements.txt
```
edit config.py file according to config-TEMPLATE.py file

For input to work in pycharm set the `Emulate terminal in output console` to true in the run configuration

## Translation

Each translateable string should be encapsulated with the _() function.

After adding new strings a new pot should be generated according to the following example of the excel src file:
```commandline
py <Location of python directory>\Tools\i18n\pygettext.py -d <namespace> -o locales/<namespace>.pot <srcfilename>.py
```
i.e.
```commandline
py C:\Users\<username>\AppData\Local\Programs\Python\Python38-32\Tools\i18n\pygettext.py -d excel -o locales/excel.pot excel.py
```

Than translate the string in the po files and run msgfmt to create the mo files:
```commandline
py <Location of python directory>\Tools\i18n\msgfmt.py -o <namespace>.mo <namespace>
```
```commandline
py C:\Users\<username>\AppData\Local\Programs\Python\Python38-32\Tools\i18n\msgfmt.py -o excel.mo excel
```

[Good tutorial](https://phrase.com/blog/posts/translate-python-gnu-gettext/)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)