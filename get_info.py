import xml.etree.ElementTree as ET
from utils import print_csv

import re


class Variable:
    def __init__(self):
        self.name = ' '
        self.description = ' '
        self.typeof = ' '
        self.isarray = False
        self.dataref = ' '
        self.ref = ' '
        self.datatype = ' '
        self.arraysize = '-'
        self.isinvisible = ' '
        self.io = ' '
        self.deleteItems = [ ]

    def set_name(self, name):
        self.name = name.lower()

    def set_description(self, description):
        self.description = description

    def set_typeof(self, typeof):

        self.typeof = typeof

    def set_isarray(self, isarray):
        #if re.match("^[a-zA-Z0-9_]*$", isarray):
            #isarray = ''.join(e for e in isarray if e.isalnum())
        self.isarray = isarray

    def set_dataref(self, dataref):
        self.dataref = dataref

    def set_ref(self, typeof):
        self.typeof = typeof

    def set_datatype(self, datatype):
        self.datatype = datatype

    def set_arraysize(self, arraysize):
        if self.arraysize and self.arraysize != '-':
            self.arraysize = self.arraysize + ', ' + arraysize
        else:
            self.arraysize = arraysize

    def set_isinvisible(self, isinvisible):
        self.isinvisible = isinvisible

    def set_io(self, io):
        self.io = io.lower()

    def set_deleteItems(self, deleteitems):
        self.deleteItems.append(deleteitems)


def container_verison(info):
    data_ref = []
    append_ref = False
    for child_data_ref in info:
        #print(child_data_ref.attrib['idref'])
        #if not append_ref:
            #data_ref.append(child_data_ref.attrib['idref'])
            #append_ref = True
        if child_data_ref.tag == 'dataobject-ref':
            str_isinvisible = ' '
            str_io = ' '
            for interior_child_data_ref in child_data_ref:
                if interior_child_data_ref.tag == 'visible':
                    str_isinvisible = interior_child_data_ref.text
                elif interior_child_data_ref.tag == 'integration':
                    str_io = interior_child_data_ref.text
            tup_data_ref = (child_data_ref.attrib['idref'], str_isinvisible, str_io)
            data_ref.append(tup_data_ref)
    return data_ref


def data_object(inf, info):
    list_traverse = [False, False, False, False]
    matrix_cond = 0
    #inf.datatype = info.attrib['type']
    inf.ref = info.attrib['id']
    for child_info in info:
        if child_info.tag == 'name':
            inf.set_name(child_info.text)
            list_traverse[0] = True
        elif child_info.tag == 'description':
            inf.set_description(child_info[0].text)
            list_traverse[1] = True
        elif child_info.tag == 'array':
            matrix_cond += 1
            inf.set_isarray(True)
            try:
                inf.set_arraysize(child_info[0].attrib['name'])
            except Exception as e:
                if not child_info.find('size'):
                    arr_val = child_info.find('size')
                    #print(test.text)
                    inf.set_arraysize(arr_val.text)
                else:
                    inf.arraysize = 'Unknown'
            #if matrix_cond == 2:
               # print('here')
                #inf.set_arraysize(arr_val.text)
            #print(child_info[0].attrib['name'])

            #list_traverse[2] = True
        elif child_info.tag == 'type':
            #inf.set_dataref(child_info.text)
            inf.set_datatype(child_info.text)
            list_traverse[3] = True
        elif child_info.tag =='displaytype-ref':
            inf.set_dataref(child_info.attrib['idref'])

        if all(list_traverse):
            break


def data_type(info):
    traverse = False
    var_reference = info.attrib['id']
    for child_datatype in info:
        if child_datatype.tag == 'basetype-ref':
            var_datatype = child_datatype.attrib['name']
            traverse = True
        if traverse:
            tup_datatype = (var_datatype, var_reference)
            break

    return tup_datatype


def data_type_action(info):
    action_name_type =[]
    for item_action in info:
        action_var_name = ' '
        if item_action.tag == 'dataobject-ref':
            action_var_name = item_action.attrib['name']
            action_integration = ' '
            for child_action in item_action:
                if child_action.tag == 'integration':
                    action_integration = child_action.text
            action_tup = (action_var_name, action_integration)
            action_name_type.append(action_tup)
    print(action_name_type)





def cross_reference(classlist, datatype, datatype_ref):
    for item in classlist:
        for tup_datatype in datatype:
            if item.dataref == tup_datatype[1]:
                item.set_typeof(tup_datatype[0])
        for tup_datatype_ref in datatype_ref:
            if item.ref == tup_datatype_ref[0]:
                item.set_io(tup_datatype_ref[2])
                item.set_isinvisible(tup_datatype_ref[1])

    return classlist


def cusf_get_info(file_loc):
    ignored_lines = ['Module Header', 'Import', 'Public Aggregate Interfaces']
    _remove_lines = []
    cusf_list = []
    append_cont = 0
    mod_name = ''
    var_list = []
    cusf_classlist = []
    not_in_contr = False
    with open(file_loc, 'r') as cusf_reader:
        while True:
            cusf_line = cusf_reader.readline()
            if 'lc_prs_air_dig_intc_mon' in cusf_line:
                print('here')
            if cusf_line.find('/*~+:') != -1:
                cond = [True for x in ignored_lines if x in cusf_line]
                if len(cond) == 0:
                    append_cont += 1
                    if append_cont > 2:
                        if len(var_list) == 0:
                            var_list = None
                        else:
                            for variables in var_list:
                                if 'lc_prs_air_dig_intc_mon' in variables:
                                    print('hge')
                                if (variables.find('(') == -1 and variables.find(')') == -1) \
                                        and variables.find('const') == -1:
                                    cusf_inf = Variable()
                                    if variables.find(' ') == 0:
                                        spacing = variables.count(' ')
                                        variables = variables[spacing - 1:]
                                    cusf_inf.typeof = variables[:variables.find(' ')]
                                    cusf_inf.name = variables[variables.find(' ') + 1:]
                                    cusf_inf.isarray = False
                                    if variables.find('[') != - 1 and variables.find(']') != -1:
                                        if variables.count('[') == 2:
                                            aux_dim_mat = variables.split('[')
                                            aux_dim_mat[1] = aux_dim_mat[1].strip(']')
                                            cusf_inf.set_arraysize(aux_dim_mat[1])
                                            cusf_inf.set_isarray(True)
                                            aux_dim_mat[2] = aux_dim_mat[2].strip(']')
                                            cusf_inf.set_arraysize(aux_dim_mat[2])
                                            #a = variables[variables.find('[') + 1: variables.find(']')]
                                            #b = variables
                                        else:
                                            cusf_inf.isarray = True
                                            cusf_inf.set_arraysize(variables[variables.find('[') + 1: variables.find(']')])
                                        try:
                                            cusf_inf.name = cusf_inf.name[:cusf_inf.name.find('[')]
                                        except Exception as e:
                                            print(e)
                                    cusf_classlist.append(cusf_inf)

                            append_cont = 1
                            mod_name = ''
                        var_list = []

            elif cusf_line.find('extern') != -1:
                try:
                    cusf_line = " ".join(cusf_line.split())

                except:
                    pass
                if cusf_line.endswith(';'):
                    cusf_line = cusf_line.strip(';')
                cusf_line = cusf_line.lstrip()
                if (cusf_line.find('(') != -1 and cusf_line.find(')') != -1) or cusf_line.find('const') != -1:
                    _remove_lines.append(cusf_line)
                #tmp = cusf_line.strip('extern')
                tmp = cusf_line[cusf_line.find(' '):]
                if tmp.find('/*') > 0:
                    tmp = tmp[:tmp.find('/*')-1]
                tmp = tmp.strip(';\n')
               # if tmp.count(' ') == 1:
                    #tmp = tmp[tmp.find(' ') + 1:]
                if tmp[0] == ' ' and 'const' in tmp:
                    tmp = tmp[1:]
                    tmp = tmp.strip('const')
                var_list.append(tmp)

            if not cusf_line:
                if not var_list is False:
                    not_in_contr = True
                    tup = ('-', var_list)
                    cusf_list.append(tup)
                    for variables in var_list:
                        cusf_inf = Variable()
                        if variables.find(' ') == 0:
                            spacing = variables.count(' ')
                            variables = variables[spacing - 1:]
                        cusf_inf.typeof = variables[:variables.find(' ')]
                        cusf_inf.name = variables[variables.find(' ') + 1:]
                        cusf_inf.isarray = False
                        if variables.find('[') != - 1 and variables.find(']') != -1:
                            cusf_inf.isarray = True
                            cusf_inf.set_arraysize(variables[variables.find('[') + 1: variables.find(']')])
                            try:
                                cusf_inf.name = cusf_inf.name[:cusf_inf.name.find('[')]
                            except Exception as e:
                                print(e)
                        cusf_classlist.append(cusf_inf)
                break

    return cusf_classlist, _remove_lines


def get_module_name(path):
    path = path.split('\\')
    module_name = path[len(path) - 1]
    module_name = module_name[:module_name.find('_')]

    return module_name.lower()


def safety_var_cutter(it):
    start_cut = it.find(',')
    aux = it[start_cut + 1:]
    second_cut = aux.find(',')
    aux = aux[:second_cut]
    aux = aux.strip()

    return aux


# Make a dictionary with the information from the C files
def make_dict(list_c):
    dict_var = {}
    lister_input = []
    lister_output = []
    lister_safety = []
    nonredundant_data = []
    for x in list_c:
        with open(x, 'r') as file_open:
            if x.find('safety') == -1:

                info_c = file_open.readlines()
                for var in info_c:
                    if var.find('SET_') != -1 and var[0]:
                        match = re.findall('SET_([a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9])', var)
                        if match:
                            #list = match.groups()
                            for var1 in match:
                                cond = [tup for tup in lister_output if tup[1] == var1]
                                if not cond:
                                    module_name = get_module_name(x)
                                    lister_output.append((module_name, var1))

                    if var.find('GET_') != -1:
                        #match = re.search(r'GET_([a-z][a-z0-9_]*[a-z0-9])', var)
                        match = re.findall(r'GET_([a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9])', var)
                        if match:
                            #list = match.groups()
                            #for var in list:
                            for var1 in match:
                                cond = [tup for tup in lister_input if tup[1] == var1]
                                if not cond:
                                    module_name = get_module_name(x)
                                    lister_input.append((module_name, var1))
            else:
                info_safey = file_open.readlines()

                # content = re.sub(r'/\*.*?\*/', '', info_safey, re.DOTALL)
                # content = re.sub(r'/\*.*?\*/','', info_safey,flags=re.DOTALL)
                for it in info_safey:
                    match = re.search(r'(\b[a-z][a-z0-9_]+_mon\b)', it)
                    if match:
                        if it.find('ACTION_ECM3_WriteChkCpl') != -1:
                            write_name = safety_var_cutter(it)
                            module_name = get_module_name(x.lower())
                            cond = [tup[1] for tup in lister_output if tup[0] == module_name and tup[1] == write_name]
                            if not cond:
                                lister_output.append((module_name, write_name))
                        elif it.find('ACTION_ECM3_ReadChkCpl') != -1:
                            write_name = safety_var_cutter(it)
                            module_name = get_module_name(x.lower())
                            cond = [tup[1] for tup in lister_input if tup[0] == module_name and tup[1] == write_name]
                            if not cond:
                                lister_input.append((module_name, write_name))

    dict_var['input'] = lister_input
    dict_var['output'] = lister_output
    return dict_var


def get_cuadp_im(_cuadp_im):
    cuadp_im_list = []
    with open(_cuadp_im, 'r') as read:
        while True:
            im_line = read.readline()
            if im_line.find('#include') != -1:
                pos_strip_start = im_line.find('<')
                pos_strip_end = im_line.find('>')
                im_stripped = im_line[pos_strip_start + 1:pos_strip_end]
                cuadp_im_list.append(im_stripped)
            if not im_line:
                break
    return cuadp_im_list


if __name__ =='__main__':
    cont_name =r'd:\Task\Task_Eugen\rec01_251.xml'
    tree = ET.parse(cont_name)
    root = tree.getroot()
    xml_info = []
    datatype = []
    data_ref = []
    print('\n')
    print("Getting data from XML file")
    print("Making a xml_info ")
    print('\n..........................')
    for child in root:
        for info in child:
            if info.tag == 'container':
                data_ref = container_verison(info)
            elif info.tag == 'dataobject':
                inf = Variable()
                data_object(inf, info)
                xml_info.append(inf)
            elif info.tag == 'displaytype':
                datatype.append(data_type(info))

    classlist = cross_reference(xml_info, datatype, data_ref)
    print_csv(xml_info, 'Verification\\xml_var.csv')
