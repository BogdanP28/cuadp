

import re
#def compile_data()
def hasNumbers(inputString):
    if any(char.isdigit() for char in inputString):
        return inputString[1:]


def check_writing(lines):
    idx = 0
    index = 0
    while index < len(lines)-1:
        if re.search('MEM_DATA MEM_DATA_PUBLIC', lines[index]):
            try:
                item_aux = lines[index]
            except Exception as e:
                pass
            aux = re.sub('\\D', '', item_aux)
            aux = str(aux)
            try:
                while not re.search('MEM_DATA MEM_DATA_PUBLIC', lines[index+1]):
                    cond = True
                    if not aux:
                        aux = 'FLAG'
                    if '<gmem.h>' in lines[index+1]:
                        tmp_val = lines[index+2]
                    else:
                        tmp_val = lines[index+1]
                    tmp_val = tmp_val.split()
                    try:
                        aux_tmp = hasNumbers(tmp_val[1])
                    except Exception as e:
                        #print('here')
                        cond = False
                    if not aux_tmp:
                        aux_tmp = tmp_val[1]
                    if aux_tmp == 'const':
                        aux_tmp = tmp_val[2]
                    if cond and aux_tmp != 'MEM_DATA':
                        if not re.search(str(aux_tmp), aux, re.IGNORECASE):
                            write_size = '#define MEM_DATA MEM_DATA_PUBLIC_' + aux_tmp
                            lines.insert(index-1, write_size)
                    index = index + 1
            except Exception as e:
                break
        index = index + 1
    writeFile(lines)



def write_cuadp(_information, cuadp_file):
    with open(cuadp_file, "r") as f:
        lines = f.readlines()
    import re
    index_inf = 0
    for idx_item, item in enumerate(_information):
        idx_item = idx_item + index_inf
        try:
            aux_item = _information[idx_item]
            aux_same_contraction = [x for x in _information if x[1] == aux_item[1]]
            aux_same_contraction = sorted(aux_same_contraction, key=lambda x: x[2])
        except Exception as e:
            pass
        first_passing = True
        index_inf = 0
        for index,  sorted_item in enumerate(aux_same_contraction):
            if first_passing == True and index_inf == 0:
                write_cond = True
                #first_passing = False
            aux = re.sub('\\D', '', sorted_item[2])
            write_size = '#define MEM_DATA MEM_DATA_PUBLIC_' + aux
            #print("aux_same_contraction[index][2]: %s -------------- aux_same_contraction[index+1][2] %s: " % (aux_same_contraction[index][2], aux_same_contraction[index+1][2]))
            try:
                if (aux_same_contraction[index][2] != aux_same_contraction[index+1][2]) and not first_passing:
                    aux_2 = re.sub('\\D', '', aux_same_contraction[index+1][2])
                    write_cond = True
            except Exception as e:
                pass

            index_line = 218
            while index_line < len(lines) - 1:
                if sorted_item[1] in lines[index_line].lower():
                    while '/*~E*/' not in lines[index_line]:
                        index_line = index_line + 1
                    if write_cond:
                        if first_passing:
                            lines.insert(index_line, write_size +'\n')
                            index_line = index_line + 1
                            write_cond = False
                            first_passing = False
                    if item[3] == '-':
                        aux = 'extern ' + str(sorted_item[2]) + ' ' + str(sorted_item[0]) + ' ' +';' + '  NEW\n'
                    else:
                        aux = 'extern ' + str(sorted_item[2]) + ' ' + str(sorted_item[0]) + '[' + str(sorted_item[3]) + ']' +';' + '  NEW\n'
                    lines.insert(index_line, aux)

                    if write_cond:
                        if not first_passing:
                            tmp = write_size
                            try:
                                write_size = '#define MEM_DATA MEM_DATA_PUBLIC_' + aux_2
                            except Exception as e:
                                write_size = tmp
                            index_line = index_line + 1
                            lines.insert(index_line, write_size +'\n')
                            index_line = index_line + 1
                            write_cond = False
                    break
                else:
                    index_line = index_line + 1
            index_inf = idx_item + len(aux_same_contraction)
    check_writing(lines)
    #writeFile(lines)


def writeFile(info):
    new_file = r"d:\PycharmProjects\Cuadp Program DemoV4\Logs\cusf_cuadp_ex_NEW.h"
    with open(new_file, 'w') as wr:
        for item in info:
            wr.write(item)


def format_cont(old_str):
    idx = 0
    new_str = ''
    for c in old_str:
        if idx == 0 or idx == 2 or idx == 5:
            new_str = new_str + c.upper()
        else:
            new_str = new_str + c
        idx = idx + 1
    return new_str


def generate_seep_format(info, cusf_file):
    cusf_file.append('/*~A*/\n')
    cont_name = '/*~+:' + format_cont(info[0][0]) + '*/\n'
    cusf_file.append(cont_name)
    if info[0][2].isalpha():
        mem_type = '#define MEM_DATA MEM_DATA_PUBLIC_' + info[0][2].upper() + '\n'
    else:
        nr = re.sub('\\D', '', info[0][2])
        mem_type = '#define MEM_DATA MEM_DATA_PUBLIC_' + nr + '\n'
    cusf_file.append(mem_type)
    cusf_file.append('#include <gmem.h>\n')
    same_code = info[0][2]
    for item in info:
        if item[2] != same_code:
            if item[2].isalpha():
                mem_type = '#define MEM_DATA MEM_DATA_PUBLIC_' + item[2].upper() + '\n'
                same_code = item[2]
            else:
                nr = re.sub('\\D', '', item[2])
                mem_type = '#define MEM_DATA MEM_DATA_PUBLIC_' + nr + '\n'
                same_code = item[2]
            cusf_file.append(mem_type)
            cusf_file.append('#include <gmem.h>\n')
        if item[3] != '-':
            aux = 'extern ' + item[2] + ' ' + item[1] + '[' + item[3] + '];\n'
        else:
            aux = 'extern ' + item[2] + ' ' + item[1] + ';\n'
        cusf_file.append(aux)
    cusf_file.append('#include <gmem.h>\n')
    cusf_file.append('/*~E*/\n')


def add_header_cusf(cusf_file, cusf_path):
    with open(cusf_path, 'r') as reader:
        line_info = reader.readline()
        stop = 'Public Aggregate Interfaces'
        stop_loop = False
        while not stop_loop:
            try:
                match = re.search(stop, line_info).group()
                if match:
                    stop_loop = True
                    cusf_file.append(line_info)
                    line_info = reader.readline()
            except Exception as e:
                cusf_file.append(line_info)
                line_info = reader.readline()
                pass


def removeDuplicates(lst):
    return list(set([i for i in lst]))


def generate(cusf_path, to_add, aws_dict, xml_info, log_path):
    list_addvar_cuadp = []
    failure_cond = False
    try:
        for tup_dict in aws_dict['input']:
            for item_xml in xml_info:
                if item_xml.name == tup_dict[1]:
                    aux_lv = tup_dict[1].split('_')
                    if aux_lv[0] == 'lv':
                        tuple_add = (tup_dict[0], tup_dict[1], 'flag', item_xml.arraysize)
                    else:
                        tuple_add = (tup_dict[0], tup_dict[1], item_xml.typeof.lower(), item_xml.arraysize)
                    list_addvar_cuadp.append(tuple_add)
    except Exception as e:
        print('Error')
        failure_cond = True
    if not failure_cond:
        for item in to_add:
            for tup in aws_dict['input']:
                if item == tup[1]:
                    for item_xml in xml_info:
                        if item_xml.name == item:
                            aux_lv = item.split('_')
                            if aux_lv[0] == 'lv':
                                tuple_add = (tup[0], item, 'flag', item_xml.arraysize)
                            else:
                                tuple_add = (tup[0], item, item_xml.typeof.lower(), item_xml.arraysize)
                            if not tuple_add in list_addvar_cuadp:
                                list_addvar_cuadp.append(tuple_add)
        sort_list = sorted(list_addvar_cuadp, key=lambda x: x[0])
        #sort_list = removeDuplicates(sort_list)
        cusf_file = []
        add_header_cusf(cusf_file, cusf_path)
        import itertools
        import operator

        for key,group in itertools.groupby(sort_list,operator.itemgetter(0)):
            group = sorted(group, key=lambda x: x[2])
            generate_seep_format(list(group), cusf_file)

        cusf_file.append('\n')
        cusf_file.append('/*~E*/\n')
        cusf_file.append('#endif\n')
        import os
        new_cuadp = os.getcwd()

        with open(log_path + 'cusf_cuadp_ex.h', 'w') as writer:
            for item in cusf_file:
                writer.write(item)
    return failure_cond

def modify_cusf(cusf_file, _remove_lines):
    with open(cusf_file, "r") as f:
        lines = f.readlines()
    new_file =r"c:\Users\uic00691\PycharmProjects\Cuadp Program DemoV3\cusf_cuadp_ex_NEW.h"
    with open(new_file, "w") as f:
        for line in lines:
            if line not in _remove_lines:
                f.write(line)