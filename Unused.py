
def comparing(classlist, var_aws):
    output_xml = [x.name.lower() for x in classlist if x.io == 'OUTPUT' and x.datatype == 'Processvariable']
    input_xml = [x.name.lower() for x in classlist if x.io == 'INPUT' and x.datatype == 'Processvariable']
    data_to_modify = []
    data_to_modify = search_dict(output_xml, var_aws['INPUT'])
    '''
    data_to_modify = search_dict(dict_var['INPUT'], output_xml)
    data_to_modify.extend(search_dict(dict_var['OUTPUT'], input_xml))
    '''
    return data_to_modify



def different(xml, cuadp):
    #xml = sorted(xml)
    #cuadp = sorted(cuadp)
    same_name = []
    with open('Same_name_diff_att.csv', mode='w') as csv_file:
        fieldnames = ['Name', 'Cuap', 'Xml']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item_xml in xml:
            for item_cuadp in cuadp:
                name_cond = False
                if item_xml[0] == item_cuadp[0]:
                    if item_xml[1] != item_cuadp[1]:
                        if not name_cond:
                            writer.writerow({'Name': item_xml[0], 'Cuap': item_cuadp[1], 'Xml': item_xml[1]})
                            name_cond = True
                        else:
                            writer.writerow({'Cuap': item_cuadp[1], 'Xml': item_xml[1]})
                    if item_xml[2] != item_cuadp[2]:
                        if not name_cond:
                            writer.writerow({'Name': item_xml[0], 'Cuap': item_cuadp[2], 'Xml': item_xml[2]})
                            name_cond = True
                        else:
                            writer.writerow({'Cuap': item_cuadp[2], 'Xml': item_xml[2]})
                    if item_xml[3] != item_cuadp[3]:
                        if not name_cond:
                            writer.writerow({'Name': item_xml[0], 'Cuap': item_cuadp[3], 'Xml': item_xml[3]})
                            name_cond = True
                        else:
                            writer.writerow({'Cuap': item_cuadp[3], 'Xml': item_xml[3]})


    print('Finish')
   # print_csv_same_name(same_name, 'same_name_diff_type.txt')

'''
def print_csv_same_name(to_print, filename = 'ceva.csv'):
    with open(filename, mode='w') as csv_file:
        fieldnames = ['Name', 'Cuap']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for x in classlist:
            # print(x.name, x.typeof, x.description, x.rangeof, x.resolution)
            writer.writerow({'Datatype': x.datatype, 'Name': x.name, 'Description': x.description, 'Typeof': x.typeof, 'isArray': x.isarray,
                                 'Array Size': x.arraysize, 'isInvisible': x.isinvisible, 'I/O': x.io, 'Dataref': x.ref})
'''


def searcher(classlist):
    lister_files = []
    #path = 'd:\\Task\\Task_Eugen\\rec01_0u0_141\\work\\ASW_RSA\\'
    #lister_files.extend(scantree(path))
    #lister = [x for x in lister_files if x.endswith('.c')]
    exH_files = [x for x in lister_files if x.endswith('_ex.h')]
    # Make a dictionary that contains information from the AWS folder
    #input_output = make_dict(lister)
    # Comparing the AWS folder with the XML File
    input_xml = [x.name.lower() for x in classlist if x.io == 'INPUT' and x.datatype == 'Processvariable']
    data_xml_aws = comparing(classlist, input_output)
    try:
        file_writer('diff_xml_aws.txt', data_xml_aws, 'Files that are in AWS folder but not in XML file\n')
    except Exception as e:
        if e == "'NoneType' object is not iterable'":
            print('All the OUTPUTS from the XML are present in the AWS .c files')

    #verify_exH_Cfile(exH_files)
