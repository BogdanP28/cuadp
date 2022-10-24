from utils import file_writer, scantree
import re

def search_dict(io, _classlist):
    try:
        break_tup = [tup[1].lower() for tup in _classlist]
    except Exception as e:
        pass
    _differences = list(set(io) - set(break_tup))
    return _differences

# Basis for different searches


def comparing(diff_xml_cuadp, var_aws, dict_info):
    data_to_modify =[]
    try:
        data_to_modify = search_dict(diff_xml_cuadp, var_aws[dict_info])
    except Exception as e:
        print('Could not find' + e)

    return data_to_modify


#def removing_special_char(lister_tuples):
   # for tup in lister_tuples:
       # if re.match("^[a-zA-Z0-9_]*$", tup[3]):
            #tup[3] = ''.join(e for e in tup[3] if e.isalnum())


def strip_location(_prj_loc):
    loc_split = _prj_loc.split('\\')
    if len(loc_split) < 2:
        loc_split = _prj_loc.split('/')

    log_name = 'Default_log'
    try:
        aux = loc_split[loc_split.index('work') -1]
        log_name = ''
        log_name = aux[:aux.find('_')] + aux[aux.rfind('_'):]
    except:
        print('Possible wrong directory. Cannont find work folder')
    return log_name


def compare_xml__cuadp(_xml_info, _cuadp, _xml_io, prj, _log_path):
    var_xml = set((x.name.lower(), x.typeof.lower(), x.isarray, x.arraysize) for x in _xml_info if x.io == _xml_io or x.io == _xml_io.lower() and x.datatype != 'Systemconstant')
    var_cuadp = set((y.name.lower(), y.typeof.lower(), y.isarray, y.arraysize) for y in _cuadp)
    difference_not_xml = [x for x in _cuadp if (x.name, x.typeof, x.isarray, x.arraysize) not in var_xml]
    difference_not_cuadp = [x for x in _xml_info if (x.name.lower(), x.typeof.lower(), x.isarray, x.arraysize) not in var_cuadp and x.io == 'input' and x.datatype != 'Systemconstant']

    var_xml_output = set((x.name.lower()) for x in _xml_info if x.io == 'output' and x.datatype != 'Systemconstant')
    # var_output_cuadp -> Variables that are Outputs in XML and are present in cuadp.ex
    var_output_cuadp = [x.name.lower() for x in difference_not_xml for out in var_xml_output if x.name == out]
    # var_local_xml contains variables that are neither declared in xml file as input or output
    var_local_xml = [x.name.lower() for x in _xml_info if x.io != 'input' and x.io != 'output']

    not_cuadp = [x.name.lower() for x in difference_not_cuadp]
    var_cuadp_names = [x[0] for x in var_cuadp]
    i = 0

    remover = []
    for item in not_cuadp:
        if item.find('lv') != -1:
            if item in var_cuadp_names:
                remover.append(item)
    not_cuadp = list((set(not_cuadp) - set(remover)))
    not_cuadp.sort()

    not_xml = [x.name.lower() for x in difference_not_xml]
    var_xml_names = [x[0] for x in var_xml]
    i = 0

    remover = []
    for item in not_xml:
        if item.find('lv') != -1:
            if item in var_xml_names:
                remover.append(item)
    not_xml = list((set(not_xml) - set(remover)))
    not_xml.sort()

    #Removing special characters
    #var_xml = [e for e in string[2] if e.isalnum() for string in var_xml if isinstance(string[2], str)]
    #removing_special_char(var_xml)
    #var_cuadp = [(string[0], string[1],''.join(e for e in string[2] if e.isalnum())) for string in var_cuadp if isinstance(string[2], str)]

    same_name_diff_att = []
    for item_name in not_cuadp:
        items = [(item_name, set(x) - set(y), set(y) - set(x)) for y in var_xml for x in var_cuadp if x[0] == y[0] and x[0] == item_name]
        if items:
            same_name_diff_att.extend(items)

    cross_checking = [tup[0] for tup in same_name_diff_att]
    not_xml = list((set(not_xml) - set(cross_checking)))
    not_cuadp = list((set(not_cuadp) - set(cross_checking)))
    #file_writer('Logs\\Same_name_diff_att.txt', same_name_diff_att, 'Same_name_diff_att\n\n.......\n')
    #file_writer('Logs\\Missing_Xml[INPUTS].txt', not_xml, 'NOT in XML[Inputs] but in Cuadp.exe\n\n.......\n')
    #file_writer('Logs\\Missing_Cuadp_ex.txt', not_cuadp, 'NOT in Cuadp.ex but in Xml[INPUTS]\n\n.......\n')

    # ----------------------------------------------------------------------------------------------------

    log_name = strip_location(prj)
    log_name = log_name + '.txt'
    import os
    try:
        if os.stat(_log_path + log_name).st_size >= 0:
            os.remove(_log_path + log_name)
    except:
        pass
    diff = list(set(not_xml) - set(var_output_cuadp))
    if not_cuadp:
        file_writer(_log_path + log_name, not_cuadp, 'Missing from Cuadp\n\n.......\n', append_rewrite_cond=1)
        file_writer(_log_path + log_name, optional_comm='\n\n----------------------------------------\n\n', append_rewrite_cond=1)
    if var_output_cuadp:
        #file_writer('Logs\\LOGS.txt', 'Variables that are Outputs in XML and are present in cuadp.ex\n\n.......\n')
        file_writer(_log_path+log_name, var_output_cuadp, 'Variables that are Outputs in XML and are present in cusf_cuadp_ex.h\n\n.......\n', append_rewrite_cond=1)
        file_writer(_log_path+log_name, optional_comm='\n\n----------------------------------------\n\n', append_rewrite_cond=1)
    if var_local_xml:
        file_writer(_log_path+log_name, var_local_xml, 'Variables declared as neither inputs or outputs in XML\n\n.......\n', append_rewrite_cond=1)
        file_writer(_log_path+log_name, optional_comm='\n\n----------------------------------------\n\n', append_rewrite_cond=1)
    if not_xml:
        file_writer(_log_path+log_name, diff, 'Inputs missing from Spec and present in cusf_cuadp_ex.h file\n\n.......\n', append_rewrite_cond=1)
        file_writer(_log_path+log_name, optional_comm='\n\n----------------------------------------\n\n', append_rewrite_cond=1)
    if same_name_diff_att:
        file_writer(_log_path+log_name, same_name_diff_att, 'Same name and different attribute\n\n.......\n', append_rewrite_cond = 1)
        file_writer(_log_path+log_name, optional_comm='\n\n----------------------------------------\n\n', append_rewrite_cond=1)

    return not_cuadp, not_xml, same_name_diff_att

'''
def differences_att(diff_list, xml_var, cuadp_var):

    xml_var_name = [tup[0] for tup in xml_var]
    cuadp_var_name = [tup[0] for tup in cuadp_var]
    xml_var_name.sort()
    not_xml = [x for x in cuadp_var_name if x not in xml_var_name]
    not_cuadp = [x for x in xml_var_name if x not in cuadp_var_name]
    not_cuadp.sort()
    full_list_diff = []
    print(list(set(diff_list) - set(not_cuadp)))
    for item_name in diff_list:
        items = [(item_name, set(x) - set(y), set(y) - set(x)) for y in xml_var for x in cuadp_var if x[0] == y[0] and x[0] == item_name]
        if items:
            full_list_diff.append(items)
    file_writer('Logs\\Missing_Xml[INPUTS].txt', not_xml, 'NOT in XML[Inputs] but in Cuadp.ex\n\n.......\n')
    file_writer('Logs\\Missing_Cuadp_ex.txt', not_cuadp, 'NOT in Cuadp.ex but in Xml[INPUTS]\n\n.......\n')

    return full_list_diff
'''

def check_cuadp(_output_xml, _cuadp_im_info, _aws_dict):

    _missing_cuadp_im = []  # List that contains missing headers
    for output_xml_var in _output_xml:
        try:
            for tuple_asw in _aws_dict['output']:
                if output_xml_var == tuple_asw[1].lower():
                    # If the value from the XML is found in ASW_RSA we search for/
                    # the module_ex.h to be included in cuadp_im.h
                    if tuple_asw[0] not in _cuadp_im_info:
                        _missing_cuadp_im.append((tuple_asw[0] + '_ex.h', tuple_asw[1]))
        except Exception as e:
            print(e)

    return _missing_cuadp_im





