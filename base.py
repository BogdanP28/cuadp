import shutil
import xml.etree.ElementTree as ET
import time
from searching import compare_xml__cuadp, comparing, check_cuadp, strip_location
from get_info import container_verison, data_object, data_type, cross_reference, cusf_get_info, Variable, make_dict, \
    get_cuadp_im, get_module_name, data_type_action
from utils import print_csv, scantree, file_writer, get_cuadp_loc, verification
import os
import sys

from Scripts.utils import get_info_from_txt
from Scripts.writing_cusf import generate
# from writing_cusf import generate
import tkinter as tk

import subprocess
import gui

# from writing_cusf import modify_cusf

'''
class noInterface():
    def __init__(self):
        self.folder_path = r'd:\p\re\c01\100\rec01_0u0_100\work'
        self.spec_name = 'WBR00101.00A'
        self.useless = 0
        self.xml_file = ' '
        self.standalone = 1

    def bar(self, val):
        self.useless = val
'''
'''
from tkinter import *


class Display(Frame):


    def __init__(self, parent=0):
        Frame.__init__(self, parent)
        win = Toplevel()
        self.entry = Entry(self)
        self.entry.pack()
        self.doIt = Button(self, text="DoIt", command=self.onEnter)
        self.doIt.pack()
        self.output = Text(self)
        self.output.pack()
        sys.stdout = self
        self.pack()

    def onEnter(self):
        print(eval(self.entry.get()))

    def write(self, txt):
        self.output.insert(END, str(txt))
'''

def base_program(obj):
    #obj2 = Display()
    # if __name__ == "__main__":
    # obj = noInterface()
    # obj.folder_path = r'd:\p\re\b00\600\reb00_0u0_600_PDS\work'
    # obj.xml_file = r'd:\Task\Task_Eugen\Xml\reb00_600.xml'
    print(obj.folder_path, obj.spec_name)
    #obj.write(obj.folder_path, obj.spec_name)
    #obj2.write(obj.folder_path)

    # obj.progress['value'] = 0
    obj.bar(20)
    start = time.time()
    diff_with_aws_input = []
    lister_aws_files = []
    aws_dict = {}
    xml_size = ''
    print('Starting program')
    #obj.write('Starting program')
    print(os.getcwd())
    #obj.write(os.getcwd())
    obj.folder_path_path = os.getcwd()
    obj.bar(20)
    # print(obj.folder_path_path)
    add_loc = "c:\\LegacyApp\\AutomotiveDataDictionary\\UCIX.exe"
    failure_cond = False
    log_name = strip_location(obj.folder_path)
    log_name = log_name + '.txt'
    log_path = obj.folder_path_path + '\\Logs\\' + log_name.strip('.txt') + '\\'
    try:
        print('Creating folders')
        os.mkdir(obj.folder_path_path + '\\Logs')
    except Exception as e:
        print('Folders already created')
    try:
        os.mkdir(log_path)
    except Exception as e:
        pass
    if len(obj.xml_file) <= 1:
        try:
            obj.spec_name_name = sys.argv[1]
        except Exception as E:
            # obj.spec_name_name = input('Enter obj.spec_name name: ')
            obj.spec_name_name = obj.spec_name
        subprocess.Popen([add_loc, "/mode:EXPORT", "/env:PROD", obj.spec_name_name,
                          obj.folder_path_path + '\\' + obj.spec_name_name + '.xml'])

        obj.folder_path_path = os.getcwd()

        # tree = ET.parse('CONTAINER_eugen.xml')
        try:
            cont_name = sys.argv[1] + '.xml'
        except Exception as e:
            cont_name = obj.spec_name_name + '.xml'
    else:
        cont_name = obj.xml_file

    time.sleep(15)
    try:
        xml_size = os.stat(cont_name)
    except Exception as e:
        print(e)
        print('Waiting for ADD to export...')
        #subprocess.Popen([add_loc, "/mode:EXPORT", "/env:PROD", obj.spec_name_name,
                          #obj.folder_path_path + '\\' + obj.spec_name_name + '.xml'])
        time.sleep(30)
        try:
            xml_size = os.stat(cont_name)
        except Exception as e:
            print(e)
            failure_cond = True
    if not xml_size:
        failure_cond = True
    if not failure_cond:
        if xml_size.st_size < 10000:
            print("Problmes with Specification")

        # cont_name ='CONTAINER_eugen.xml'
        tree = ET.parse(cont_name)
        root = tree.getroot()
        xml_info = []
        datatype = []
        data_ref = []
        print('\n')
        print("Getting data from XML file")
        print("Making a xml_info ")
        print('\n..........................')
        # obj.bar(20)
        for child in root:
            for info in child:
                if info.tag == 'container':
                    data_ref = container_verison(info)
                elif info.tag == 'dataobject':
                    inf = Variable()
                    data_object(inf, info)
                    if inf.datatype == 'Action-Parameter':
                        del inf
                    else:
                        xml_info.append(inf)
                elif info.tag == 'displaytype':
                    datatype.append(data_type(info))
                # elif info.tag == 'action':
                # data_type_action(info)

        xml_info = cross_reference(xml_info, datatype, data_ref)
        # obj.folder_path_loc = input('Enter location of the project: ')
        obj.folder_path_loc = obj.folder_path
        input_loc = get_cuadp_loc(obj.folder_path_loc)

        obj.bar(20)
        # cusf_ex_loc = 'd:\\Task\\Task_Eugen\\rec01_0u0_141\\work\\aggr\\cusf\\agf\\cusf_cuadp_ex\\i\\cusf_cuadp_ex.h'
        # cusf_im_loc = 'd:\\Task\\Task_Eugen\\rec01_0u0_141\\work\\aggr\\cusf\\agf\\cusf_cuadp_im\\i\\cusf_cuadp_im.h'

        cusf_ex_loc = [x for x in input_loc if x.endswith('_ex.h')]
        cusf_ex_loc = cusf_ex_loc[0]

        cusf_im_loc = [x for x in input_loc if x.endswith('_im.h')]
        cusf_im_loc = cusf_im_loc[0]

        # cusf_ex_loc = obj.folder_path_loc + 'aggr\\cusf\\agf\\cusf_cuadp_ex\\i\\cusf_cuadp_ex.h'
        # -------------------------------------- Getting cusf_cuadp variables ------------------------------------------
        cuadp_ex_info, remove_lines = cusf_get_info(cusf_ex_loc)
        # modify_cusf(r"c:\Users\uic00691\PycharmProjects\Cuadp Program DemoV3\cusf_cuadp_ex.h", _
        # remove_lines=remove_lines)
        # Comparing XML file with cuadp_ex file
        # cuadp_diff_ex - missing cuadp \\\\\\\\\\\\ xml_diff_ex = not xml \\\\\\ attrib_diff_ex = same name diff attrib
        cuadp_diff_ex, xml_diff_ex, attrib_diff_ex = compare_xml__cuadp(xml_info, cuadp_ex_info, 'input',
                                                                        obj.folder_path, log_path)

        print("Analyzing AWS Folder")
        if cuadp_diff_ex:
            lister_aws_files = []
            path = obj.folder_path_loc
            try:
                lister_aws_files.extend(scantree(path + r'/ASW_RSA'))
            except Exception as e:
                print(e)
                try:
                    lister_aws_files.extend(scantree(path + r'/work' + r'/ASW_RSA'))
                except Exception as e:
                    print(e)
                    print('Wrong directory')
            lister_cfiles = [x for x in lister_aws_files if x.endswith('.c')]
            aws_dict = make_dict(lister_cfiles)

        print('Generating cusf_cuadp.ex file')

        # ---------------------------------------------------------- Text generating -----------------------------------
        # cusf_file = r'd:\p\re\c01\100\rec01_0u0_100\work\aggr\cusf\agf\cusf_cuadp_ex\i\cusf_cuadp_ex.h '
        cusf_file = obj.folder_path + r'\aggr\cusf\agf\cusf_cuadp_ex\i\cusf_cuadp_ex.h'
        if obj.standalone == 1:
            failure_cond = generate(cusf_file, cuadp_diff_ex, aws_dict, xml_info, log_path)

    if not failure_cond:
        #print('\n...')
        obj.bar(20)
        # print('\n')
        # print("Printing the differences")
        # print('\n..........................')

        cuadp_im_info = get_cuadp_im(cusf_im_loc)

        lister_exh_files = []
        for files in lister_aws_files:
            if files.endswith('_ex.h'):
                mod_name = get_module_name(files)
                lister_exh_files.append(mod_name.lower())

        cuadp_im_info = [x.strip('_ex.h') for x in cuadp_im_info]
        cuadp_im_info = [x.lower() for x in cuadp_im_info]
        # print(list(set(cuadp_im_info) - set(lister_exh_files)))
        # print(list(set(lister_exh_files) - set(cuadp_im_info)))

        output_xml = [x.name.lower() for x in xml_info if x.io == 'output']

        # This will be used for the standalone version
        if obj.standalone == 1:
            try:
                if os.stat(log_path + 'Standalone ' + log_name).st_size >= 0:
                    os.remove(log_path + 'Standalone ' + log_name)
            except:
                pass
            try:
                diff_with_aws_input = comparing(cuadp_diff_ex, aws_dict, 'input')
            except Exception as e:
                print(e)
            try:
                # diff_xml_out_dict = comparing(output_xml, aws_dict, 'output')  # This contains elements that are in AWS but not in XML[OUTPUTS]
                aux_dict_input = aws_dict['input']
                names_common = [x[1] for x in aux_dict_input if x[1].islower()]
                xml_names = [x.name.lower() for x in xml_info]
                diff_xml_out_dict = set(names_common) - set(xml_names)
            except Exception as e:
                print(e)

            try:
                file_writer(log_path + 'Standalone ' + log_name, diff_xml_out_dict,
                            optional_comm='Inputs that are missing from the spec (if they are used in ASW_RSA, they should be present in the specification and cusf_cuadp_ex.h)\n\n........\n',
                            append_rewrite_cond=1)
                file_writer(log_path + 'Standalone ' + log_name, diff_with_aws_input,
                            optional_comm='\n........\nVariables that are missing from ASW_RSA folder and Cuadp.ex\n',
                            append_rewrite_cond=1)
                file_writer(log_path + 'Standalone ' + log_name, list(set(cuadp_diff_ex) - set(diff_with_aws_input)),
                            optional_comm='\n........\nVariables that are present in both XML and ASW_RSA but are missing from cusf_cuadp_ex.h \n',
                            append_rewrite_cond=1)
            except Exception as e:
                print(e)

        # Checking if xml_output is in asw_out and then if the module is in cuadp_im.h
        missing_cuadp_im = check_cuadp(output_xml, cuadp_im_info, aws_dict)  # List that contains missing headers

        file_writer(log_path + 'Missing_cuadp_im_' + log_name, missing_cuadp_im,
                    'The headers that are missing from the cuadp_im.h and the variables that are used in ASW_RSA\n\n')
        get_info_from_txt(log_path)

        print('\n')
        print("Searching")
        print('\n..........................')

        obj.bar(20)
        end = time.time()

        #verification(xml_info, aws_dict, cuadp_ex_info, cuadp_im_info, obj.folder_path_path)

        print('Execution time: ', end - start)
        try:
            shutil.move(cont_name, log_path)
        except:
            pass
        try:
            shutil.move(cont_name.strip('.xml') + '.log', log_path)
        except:
            pass
        print("Program has finish execution")
        obj.finish("Program has finish succesfully\nLog path: " + log_path[:-1])
        obj.log_path = log_path

    else:
        print("Program failed its execution")
        obj.finish("Program failed its execution. Check specification file and project folder")
        obj.bar(0)
