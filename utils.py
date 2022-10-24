from html.parser import HTMLParser
from os import curdir, scandir
import typing
import csv
import fnmatch
from os.path import basename
from os import walk, mkdir
import xlsxwriter

DEFAULT_SKIP_LIST = ['.git', '.hg']
SkipList = typing.Optional[typing.List[str]]

pstring = source_code = 'CONTAINER_eugen.htm'

# Searchig the project for the path of the cusf_cuadp_ex.h and cusf_cuadp_im.h
def get_cuadp_loc(_prj_loc):
    loc_cuadp = []
    for root, dirs, files in walk(_prj_loc):
        for name in files:
            if name == 'cusf_cuadp_ex.h' or name == 'cusf_cuadp_im.h':
                loc_cuadp.append(root + '\\' + name)
    return loc_cuadp

def write_new_file(file_name, _data = [], optional_comm=''):
    with open(file_name, 'w') as _writer:
        if optional_comm:
            _writer.write(optional_comm)
        if _data:
            for _item in _data:
                try:
                    _writer.write(_item)
                except Exception as e:
                    try:
                        _writer.write('\n'.join('%s %s' % x for x in _data))
                    except Exception as e:
                        _writer.write('\n'.join('%s %s %s' % x for x in _data))
                    break
                _writer.write('\n')

def file_writer(file_name, _data = [], optional_comm='', append_rewrite_cond=0):
    if append_rewrite_cond:
        try:
            with open(file_name, 'a') as _writer:
                if optional_comm:
                    _writer.write(optional_comm)
                if _data:
                    for _item in _data:
                        try:
                            _writer.write(_item)
                        except Exception as e:
                            try:
                                _writer.write('\n'.join('%s %s' % x for x in _data))
                            except Exception as e:
                                _writer.write('\n'.join('%s %s %s' % x for x in _data))
                            break

                        _writer.write('\n')
        except:
            write_new_file(file_name, _data, optional_comm)
    else:
        write_new_file(file_name, _data, optional_comm)


def print_csv(classlist, filename = 'ceva.csv'):
    classlist = sorted(classlist, key=lambda x: x.datatype, reverse=False)
    with open(filename, mode='w') as csv_file:
        fieldnames = ['Datatype', 'Name', 'Description', 'Typeof', 'isArray', 'Array Size', 'isInvisible', 'I/O', 'Dataref']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for x in classlist:
            # print(x.name, x.typeof, x.description, x.rangeof, x.resolution)
            writer.writerow({'Datatype': x.datatype, 'Name': x.name, 'Description': x.description, 'Typeof': x.typeof, 'isArray': x.isarray,
                                 'Array Size': x.arraysize, 'isInvisible': x.isinvisible, 'I/O': x.io, 'Dataref': x.ref})


class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
        super().__init__()
        self.fed = []

    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)

    def handle_data(self, data):
        self.HTMLDATA.append(data)

    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []


def scantree(path_name, skip_list=None):
    if skip_list is None:
        skip_list = DEFAULT_SKIP_LIST

    try:
        for entry in (e for e in scandir(path_name)
                      if not is_ignored(e.path, skip_list)):
            if entry.is_dir(follow_symlinks=False):
                yield from scantree(entry.path, skip_list)
            else:
                yield entry.path
    except PermissionError:
        yield 'PermissionError reading {}'.format(path_name)


def is_ignored(name: str, ignore_list: typing.List[str]) -> bool:
    """checks if file name matches the ignore list"""
    name = basename(name)
    return bool(any(fnmatch.fnmatch(name, p) for p in ignore_list))


if __name__ == '__main__':
    with open(r'CONTAINER_eugen.htm', "r") as f:
        page = f.read()
    # print(page)
    parser = myhtmlparser()
    parser.feed(page)

    # Extract data from parser
    tags = parser.NEWTAGS
    attrs = parser.NEWATTRS
    data = parser.HTMLDATA

    # Clean the parser
    parser.clean()
    # Print out our data
    # print(tags)
    data_clean = [x for x in data if x.count('_') > 1]
    data_clean = [x[:-2] for x in data_clean]

    print(data_clean)
    with open("export_html.txt", 'w+') as writer:
        for item in data_clean:
            writer.write(item)
            writer.write('\n')


def verification(xml_info, aws_dict, cuadp_ex_info, cuadp_im_info, prj_path):
    try:
        print('Creating folders')
        mkdir(prj_path + '\\Verification')
    except Exception as e:
        print('Folders already created')

    print_csv(xml_info, 'Verification\\xml_var.csv')
    print('\n')
    print("Printing the information from the AWS_RSA files")
    print('\n..........................')
    try:
        file_writer('Verification\\GET_AWS.txt', aws_dict['input'], 'GETS IN AWS\n')
        file_writer('Verification\\SET_AWS.txt', aws_dict['output'], 'SETS IN AWS\n')
    except Exception as e:
        print(e)

    #file_writer('Verification\\GET_AWS.txt', aws_dict['INPUT'], 'GETS IN AWS\n')
    print('\n')
    print("Printing the information of CUADP file for verification")
    print('\n..........................')
    print_csv(cuadp_ex_info, 'Verification\\cuadp_ex_var.csv')

    file_writer('Verification\\cuadp_im_info.csv', cuadp_im_info, 'Imports in cusf_cuadp_im')


def get_col_widths(workbook):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in workbook.index.values] + [len(str(workbook.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in workbook[col].values] + [len(col)]) for col in workbook.columns]


def excel_writer(log_file, d):
    myFile = log_file + r"\data.xlsx"
    key_list = list(d.keys())
    val_list = list(d.values())

    workbook = xlsxwriter.Workbook(myFile)
    worksheet = workbook.add_worksheet()

    # Start from the first cell.
    # Rows and columns are zero indexed.
    row = 0
    column = 0

    for item_key, item_value in zip(key_list, val_list):
        row = 0
        worksheet.set_column('{0}:{0}'.format(chr(column + ord('A'))), len(str(item_key)) + 8)
        worksheet.write(row, column, item_key)
        row += 1
        for el in item_value:
            worksheet.write(row, column, el)
            row += 1
        column += 1
    workbook.close()




#def get_col_widths(dataframe):


def get_info_from_txt(log_file):
    import glob, os
    #os.chdir(log_file)
    info_csf = []
    cusf_info = {}
    list_var = []
    for file in glob.glob(log_file + r"\*.txt"):
        with open(file, 'r') as reader:
            line = reader.readline()
            csv_headline = ''
            list_var = []

            ct = 0
            while line:
                if line[0].isupper():
                    if ct > 0:
                        cusf_info[csv_headline] = list_var
                        list_var = []
                    csv_headline = line
                    ct = ct + 1
                    line = reader.readline()
                else:
                    if line != '\n' and not '...' in line:
                        list_var.append(line.strip('\n'))
                    line = reader.readline()

            if ct == 1:
                cusf_info[csv_headline] = list_var
                list_var = []
        cusf_info[csv_headline] = list_var
    #cusf_info[csv_headline] = list_var
    import collections
    od = collections.OrderedDict(sorted(cusf_info.items()))
    excel_writer(log_file, od)
