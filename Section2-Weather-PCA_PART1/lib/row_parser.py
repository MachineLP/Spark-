import numpy as np
from pyspark.sql import Row, SQLContext,DataFrame
from pyspark.sql.types import *
import datetime as dt

def packArray(a):
    if type(a)!=np.ndarray:
        raise Exception("input to packArray should be numpy.ndarray. It is instead "+str(type(a)))
    return bytearray(a.tobytes())
def unpackArray(x,data_type=np.int16):
    return np.frombuffer(x,dtype=data_type)

def init_parser_parameters():
    def parse_date(s):
        return dt.datetime.strptime(s,'%Y-%m-%d %H:%M:%S.%f')
    def parse_array(a):
        np_array=np.array([np.float64(x) for x in a])
        return packArray(np_array)
    def parse_int(s):
        return int(s)
    def parse_float(s):
        return float(s)
    def parse_string(s):
        return(s)



    Fields=[('time', 'datetime'),
        ('species', 'str'),
        ('site', 'str'),
        ('rec_no', 'str'),
        ('bout_i', 'int'),
        ('peak2peak', 'float'),
        ('MSN', 'array',202),
        ('MSP', 'array',101),
        ('TPWS1', 'bool'),
        ('MD1', 'bool'),
        ('FD1', 'bool'),
        ('TPWS2', 'bool'),
        ('MD2', 'bool'),
        ('FD2', 'bool'),
        ('TPWS3', 'bool'),
        ('MD3', 'bool'),
        ('FD3', 'bool')]

    global Parse_rules, RowObject
    #prepare date structure for parsing
    Parse_rules=[]
    index=0
    for field in Fields:
        _type=field[1]
        #print(_type)
        _len=1 # default length in terms of csv fields
        if _type =='array': 
            parser=parse_array
            _len=int(field[2])
        elif _type=='datetime': 
            parser=parse_date
        elif _type=='int': 
            parser=parse_int
        elif _type=='float': 
            parser=parse_float
        elif _type=='bool': 
            parser=parse_int
        elif _type=='str': 
            parser=parse_string
        else:
            print('unrecognized type',_type)
        rule={'name':field[0],
              'start':index,
              'end':index+_len,
              'parser':parser}
        print(field,rule)
        Parse_rules.append(rule)
        index+=_len

    field_names=[a['name'] for a in Parse_rules]
    RowObject= Row(*field_names)
    return Parse_rules,field_names,RowObject

def parse(row):
    global Parse_rules, RowObject
    items=row.split(',')
    D=[]
    for pr in Parse_rules:
        start=pr['start']
        end=pr['end']
        parser=pr['parser']
        if end-start==1:
            D.append(parser(items[start]))
        else:
            D.append(parser(items[start:end]))
    return RowObject(*D