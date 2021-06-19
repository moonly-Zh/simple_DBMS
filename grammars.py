import ply.yacc as yacc
from Lex import tokens
import os
import re
import shutil  # 删除非空目录的函数 rmtree

root = 'DBMS'
conf = 'sys.dat'
current_db = ''


#################################################################33
# 数据库操作函数定义

# 检查已存在的数据库并返回
def check_db():
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(os.path.join(root, conf)):
        open(os.path.join(root, conf), 'w')
        return []
    fp = open(os.path.join(root, conf), 'r')
    names = [name.strip() for name in fp.readlines() if name]
    fp.close()
    return names


# 创建数据库
def create_db(name):
    exisNames = check_db()
    if name in exisNames:
        return False
    fp = open(os.path.join(root, conf), 'a')
    fp.write(name + '\n')
    fp.close()
    os.mkdir(os.path.join(root, name))
    open(os.sep.join([root, name, conf]), 'w')
    return True


# 显示所有数据库
def show_db(names):
    print(names)


# 删除某个数据库
def drop_db(name):
    names = check_db()
    if name not in names: return False
    names.remove(name)
    fp = open(os.path.join(root, conf), 'w')
    for s in names:
        fp.write(s + '\n')
    fp.close()
    shutil.rmtree(os.path.join(root, name))  # 能够删除非空目录
    return True


######################################################
def check_tb():
    global current_db
    if current_db == '':
        print('未选中数据库！')
        return False
    tb_root = os.sep.join([root, current_db])
    if not os.path.exists(os.path.join(tb_root, conf)):
        print('找不到配置文件', os.path.join(tb_root, conf))
        return
    tbs = {}
    fp = open(os.path.join(tb_root, conf), 'r')
    for line in fp.readlines():
        s = line.strip().split()
        tmp = {'name': s[2]}
        tmp['prop'] = {'type': s[3]}
        if len(s) != 4:
            tmp['prop']['len'] = int(s[4])
        if int(s[1]) == 1:
            tbs[s[0]] = []
        tbs[s[0]].append(tmp)
    fp.close()
    # 检查配置文件中的表格是否存在
    tmp = list(tbs.keys())
    for tb_name in tmp:
        if not os.path.exists(os.path.join(tb_root, tb_name + '.txt')):
            tbs.pop(tb_name)
    # 检查当前目录中的txt文件是否都在dat中声明
    tb_names = [t[:-4] for t in os.listdir(tb_root) if t[-3:] == 'txt']
    for t in tb_names:
        if tbs.get(t) == None:
            os.remove(os.path.join(tb_root, t + '.txt'))
    write_tb_conf(tbs)

    # print(tbs)
    return tbs


# 写table的conf的函数
def write_tb_conf(tbs):
    if current_db == '':
        print('未选中数据库！')
        return False
    tb_root = os.sep.join([root, current_db])
    fp = open(os.path.join(tb_root, conf), 'w')
    for tb_name, tb_elements in tbs.items():
        for i in range(len(tb_elements)):
            if tb_elements[i]['prop'].get('len'):
                fp.write('%s %d %s %s %d\n' % (tb_name, i + 1, tb_elements[i]['name'],
                                               tb_elements[i]['prop']['type'],
                                               tb_elements[i]['prop']['len']))
            else:
                fp.write('%s %d %s %s\n' % (tb_name, i + 1, tb_elements[i]['name'],
                                            tb_elements[i]['prop']['type']))
    fp.close()


# table 函数定义
def create_tb(name, elements_list):
    tbs = check_tb()
    if not tbs: return
    tb_root = os.sep.join([root, current_db])
    if tbs.get(name):
        print('该表已经存在请重新输入表名')
        return False
    tbs[name] = elements_list
    # 写新表到配置文件
    write_tb_conf(tbs)
    open(os.path.join(tb_root, name + '.txt'), 'w')
    # print(tbs)
    return True
    print({name: elements_list})


# 输入字符串列表 根据conf输出正确格式的字符串列表
def format_data(data_old, conf, col_list=[]):
    data_new = []
    for i in range(len(conf)):
        if col_list == []:
            idx = i
        else:
            idx = col_list.index(conf[i]['name'])
        if conf[i]['prop']['type'] == 'int':
            data_new.append(int(data_old[idx]))
        elif conf[i]['prop']['type'] == 'float':
            data_new.append(float(data_old[idx]))
        elif conf[i]['prop']['type'] == 'char':
            data_new.append(data_old[idx])
    return data_new


# 读某个表
def read_tb(name, conf):
    tb_root = os.sep.join([root, current_db])
    fp = open(os.path.join(tb_root, name + '.txt'), 'r')
    data = []
    for line in fp.readlines():
        s = line.strip().split()
        data.append(format_data(s, conf))
    fp.close()
    return data


#写表
def write_tb(tb, name, conf):
    tb_root = os.sep.join([root, current_db])
    fp = open(os.path.join(tb_root, name + '.txt'), 'w')
    for data in tb:
        fp.write(' '.join([str(tmp) for tmp in data]))
        fp.write('\n')
    fp.close()


#insert插入
def insert_into_tb(tb_name, value_list, column_list=[]):
    # global current_db
    # if current_db == '':
    #     print('未选中数据库！')
    #     return False
    # tb_root = os.sep.join([root, current_db])
    tbs = check_tb()
    if not tbs: return
    if tb_name not in tbs.keys():
        print('该表不存在，请重新输入表名！')
        return
    tb = read_tb(tb_name, tbs[tb_name])
    # print(tb)
    for value in value_list:
        tb.append(format_data(value, tbs[tb_name], column_list))
    # print(tb)
    write_tb(tb, tb_name, tbs[tb_name])


#选择表
def select_tb(tb_name, col_list, condition=None):
    tbs = check_tb()
    if not tbs: return
    if tb_name not in tbs.keys():
        print('该表不存在，请重新输入表名！')
        return
    conf = tbs[tb_name]
    tb = read_tb(tb_name, conf)
    ans = []
    for data in tb:
        d_data = {}
        for i in range(len(data)):
            d_data[conf[i]['name']] = data[i]
        if condition == None or condition(d_data):
            ans.append(d_data)
    for an in ans:
        if col_list == ['*']:
            print(an)
        else:
            for col in col_list:
                print(col + ' : ' + str(an[col]), end='\t')
            print()



#update更新表中元素
def update_tb(tb_name, set_list, condition):
    tbs = check_tb()
    if not tbs: return
    if tb_name not in tbs.keys():
        print('该表不存在，请重新输入表名！')
        return
    conf = tbs[tb_name]
    tb = read_tb(tb_name, conf)
    # print(set_list)
    for data in tb:
        d_data = {}
        for i in range(len(data)):
            d_data[conf[i]['name']] = data[i]
        # if condition(d_data)
        d_data.update(set_list)
        for idx in range(len(data)):
            if conf[idx]['prop']['type'] == 'int':
                data[idx] = int(d_data[conf[idx]['name']])
            else:
                data[idx] = d_data[conf[idx]['name']]
    # print(tb)
    write_tb(tb, tb_name, conf)



#delete删除表中元素
def delete_tb(tb_name, condition=None):
    tbs = check_tb()
    if not tbs: return
    if tb_name not in tbs.keys():
        print('该表不存在，请重新输入表名！')
        return
    conf = tbs[tb_name]
    tb = read_tb(tb_name, conf)
    for data in tb:
        d_data = {}
        for i in range(len(data)):
            d_data[conf[i]['name']] = data[i]
        if condition == None or condition(d_data):
            del tb[tb.index(data)]
    # print(tb)
    write_tb(tb, tb_name, conf)


#drop废弃表
def drop_tb(tb_name):
    tbs = check_tb()
    if not tbs: return
    if tb_name not in tbs.keys():
        print('该表不存在，请重新输入表名！')
        return
    del tbs[tb_name]
    write_tb_conf(tbs)
    check_tb()


###########################################################
# 语法定义
def p_statement(p):
    '''
    statement   : database_statement SEMICOLON
                | table_statement SEMICOLON
    '''
    pass


###########################################################
# database 语法定义

#create创建
def p_database_statement_c(p):
    'database_statement  : CREATE DATABASE ID'
    if not create_db(p[3]):
        print('新建数据库失败，该数据库已经存在')

#select选择
def p_database_statement_s(p):
    'database_statement  : SHOW DATABASES'
    show_db(check_db())

#update更新
def p_database_statement_u(p):
    'database_statement : USE ID'
    global current_db
    current_db = p[2]

#delete删除
def p_database_statement_d(p):
    'database_statement : DROP DATABASE ID'
    if not drop_db(p[3]):
        print('删除数据库失败，请检查%s是否存在' % (p[2]))


##################################################################
# table 语法定义

def p_table_statement_create(p):
    'table_statement : CREATE TABLE ID LPAREN base_elements_list RPAREN'
    if not create_tb(p[3], p[5]):
        print('创建失败')


def p_base_elements_list(p):
    '''
    base_elements_list  : base_element
                        | base_elements_list COMMA base_element
    '''
    p[0] = []
    if len(p) == 2:
        p[0].append(p[1])
    else:
        p[0].extend(p[1])
        p[0].append(p[3])
        # print(p[0])


def p_base_element(p):
    'base_element    : ID data_type'
    p[0] = {}
    p[0]['name'] = p[1]
    p[0]['prop'] = p[2]
    # print(p[0]['prop']['type'])


def p_data_type(p):
    '''data_type    : CHAR LPAREN NUM RPAREN
                    | INT
                    | FLOAT
    '''
    p[0] = {}
    p[0]['type'] = p[1]
    if len(p) == 5:
        p[0]['len'] = int(p[3])
    # print(p[0])


# 在表格中插入元素
def p_table_statement_insert(p):
    '''
    table_statement :   INSERT INTO ID LPAREN opt_column_list RPAREN VALUES  insert_values_list
                    |   INSERT INTO ID  VALUES  insert_values_list
    '''
    if len(p) == 6:
        insert_into_tb(p[3], p[5])
        # print(p[3], p[5])
    else:
        insert_into_tb(p[3], p[8], p[5])
        # print(p[3], p[8], p[5])


def p_opt_column_list(p):
    '''
    opt_column_list     :   ID
                        |   opt_column_list COMMA ID
    '''
    p[0] = []
    if len(p) == 2:
        p[0].append(p[1])
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_insert_values_list(p):
    '''
    insert_values_list  : LPAREN insert_value RPAREN
                        | insert_values_list COMMA LPAREN insert_value RPAREN
    '''
    p[0] = []
    if len(p) == 4:
        p[0].append(p[2])
        # print(p[0])
    else:
        # print(p[1])
        p[1].append(p[4])
        p[0] = p[1]


def p_insert_value(p):
    '''
    insert_value    : base_value
                    | insert_value COMMA base_value
    '''
    p[0] = []
    if len(p) == 2:
        p[0].append(p[1])
        # print(p[1])
    else:
        # print(p[3])
        p[1].append(p[3])
        p[0] = p[1]
    # print(p[0])


def p_base_value(p):
    '''
    base_value  : NUM
                | QUOTE ID QUOTE
                | DQUOTE ID DQUOTE
                | ID_NUM
    '''
    if len(p) == 2:
        if p.slice[1].type == 'NUM':
            p[0] = p[1]
        else:
            p[0] = p[1][1:-1]
    else:
        p[0] = p[2]



def p_table_statement_select(p):
    '''
    table_statement    : SELECT sel_col_list FROM ID
                        | SELECT sel_col_list FROM ID WHERE condition
    '''
    if len(p) == 5:
        select_tb(p[4], p[2])
    else:
        select_tb(p[4], p[2], p[6])


def p_sel_col_list(p):
    '''
    sel_col_list    : sel_col_list COMMA ID
                    | ID
                    | '*'
    '''
    p[0] = []
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0].append(p[1])


def p_where_condition(p):
    '''
    condition   : condition OR and_condition
                | and_condition
    '''
    if len(p) == 4:
        p1, p2 = p[1], p[3]
        p[0] = lambda data: p1(data) or p2(data)
    else:
        p[0] = p[1]


def p_and_condition(p):
    '''
    and_condition   : and_condition AND factor
                    | factor
    '''
    if len(p) == 4:
        p1, p2 = p[1], p[3]
        p[0] = lambda data: p1(data) and p2(data)
    else:
        p[0] = p[1]


def p_factor(p):
    '''
    factor  : ID_factor
            | NUM_factor
            | LPAREN condition RPAREN
            | NOT factor
    '''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p1 = p[2]
        p[0] = lambda data: not p1(data)
    else:
        p[0] = p[1]


def p_ID_factor(p):
    '''
    ID_factor   : ID '=' QUOTE ID QUOTE
                | ID '=' DQUOTE ID DQUOTE
                | ID '=' ID_NUM
                | ID LIKE QUOTE ID QUOTE
                | ID LIKE DQUOTE ID DQUOTE
                | ID LIKE ID_NUM
    '''
    targe = ''
    if len(p) == 4:
        targe = p[3][1:-1]
    else:
        targe = p[4]
    if p[2] == '=':
        p1 = p[1]
        p[0] = lambda data: data[p1] == targe
    else:
        targe = targe.replace('.', '\.')
        targe = targe.replace('%', '.*')
        pattern = re.compile(targe)
        p1 = p[1]
        p[0] = lambda data: pattern.match(data[p1]) is not None


def p_NUM_factor(p):
    '''
    NUM_factor   : ID '=' NUM
                | ID DE NUM
                | ID '>' NUM
                | ID GE NUM
                | ID '<' NUM
                | ID LE NUM
    '''
    col = p[1]
    targe = p[3]-1
    opt = [2]
    if opt == '=':
        p[0] = lambda data: data[col] == targe
    elif opt == 'DE':
        p[0] = lambda data: data[col] != targe
    elif opt == '>':
        p[0] = lambda data: data[col] > targe
    elif opt == 'GE':
        p[0] = lambda data: data[col] >= targe
    elif opt == '<':
        p[0] = lambda data: data[col] < targe
    elif opt == 'LE':
        p[0] = lambda data: data[col] <= targe


def p_table_statement_update(p):
    '''
    table_statement :   UPDATE ID SET set_list  WHERE condition
    '''
    update_tb(p[2], p[4], p[6])


def p_set_list(p):
    '''
    set_list    : set_list COMMA set_atom
                | set_atom
    '''
    if len(p) == 4:
        p[1].update(p[3])
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_set_atom(p):
    '''
    set_atom    : ID '=' QUOTE ID QUOTE
                | ID '=' DQUOTE ID DQUOTE
                | ID '=' ID_NUM
                | ID '=' NUM
    '''
    p[0] = {}
    if len(p) == 6:
        p[0][p[1]] = p[4]
    else:
        if p.slice[3].type == 'NUM':
            p[0][p[1]] = p[3]
        else:
            p[0][p[1]] = p[3][1:-1]


def p_table_statement_delete(p):
    '''
    table_statement : DELETE FROM ID WHERE condition
                    | DELETE FROM ID
    '''
    if len(p) == 6:
        delete_tb(p[3], p[5])
    else:
        delete_tb(p[3])


def p_table_statement_drop(p):
    '''
    table_statement :   DROP TABLE ID
    '''
    drop_tb(p[3])


###################################################################
def p_error(p):
    if p:
        print('语法解析错误：', p.type)
    else:
        print('请检查分号')


yacc.yacc()
