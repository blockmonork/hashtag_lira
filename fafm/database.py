import mysql.connector
from collections import namedtuple
import time
import datetime


class Database:

    theDefaults = namedtuple(
        'defaults', ['database', 'host', 'user', 'password'])
    defaults = theDefaults('normatel2', 'localhost', 'fafm', 'fafm1234')

    database = ''
    host = ''
    user = ''
    password = ''
    db = ''
    campos = []
    valores = []

    def __init__(self, database='', host='', user='', password=''):
        self.database = database if database != '' else self.defaults.database
        self.host = host if host != '' else self.defaults.host
        self.user = user if user != '' else self.defaults.user
        self.password = password if password != '' else self.defaults.password
        self.connect()

    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        if self.db == None:
            print('error connection')

    def select_free(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def select(self, field, table, where='1'):
        sql = f'SELECT {field} FROM {table} WHERE {where};'
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
    def count(self, table, where='1'):
        sql = f'SELECT COUNT(*) AS x FROM {table} WHERE {where}'
        result = self.select_free(sql)
        return result[0][0]

    def detect_type(self, val):
        if '-' in str(val):
            p = str(val).split('-')
            if len(p[0]) == 4 and len(p[1]) == 2 and len(p[2]) == 2:
                return self.date_to_timestamp(val)

        if self.is_number(val) or self.is_bool(val):
            return val
        else:
            return "'" + str(val) + "'"

    def date_to_timestamp(self, data):
        return int(time.mktime(datetime.datetime.strptime(data, "%Y-%m-%d").timetuple()))

    def extract(self, val):
        r = ''
        for i in val:
            r += str(i) + ','
        return r[:len(r)-1]

    def insert(self, tabela, dict_key_value):
        self.campos = []
        self.valores = []
        i = 0
        for x in dict_key_value:
            i += 1
            for y in x:
                self.campos.append(str(y))
                self.valores.append(self.detect_type(x[y]))

        if len(self.campos) > 0 and len(self.valores) == len(self.campos):
            self.executar(
                f"INSERT INTO {tabela} ( {self.extract(self.campos)} ) VALUES ( {self.extract(self.valores)} ); "
            )

    def update(self, tabela, dict_key_value, str_where):
        self.campos = []
        self.valores = []
        i = 0
        for x in dict_key_value:
            i += 1
            for y in x:
                self.valores.append(str(x) + '=' + self.detect_type(x[y]))

        if len(self.valores) > 0:
            self.executar(
                f'UPDATE {tabela} SET {self.extract(self.valores)} WHERE {str_where}'
            )

        self.otimizar(tabela)

    def delete(self, tabela, where):
        query = f'DELETE FROM {tabela} WHERE {where}'
        self.executar(query)
        self.otimizar(tabela)

    def executar(self, query):
        with self.db.cursor() as cursor:
            cursor.execute(query)
            self.db.commit()

    def otimizar(self, tabela):
        # avoid error no result set
        # https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
        cursor = self.db.cursor(buffered=True)
        cursor.execute(f'OPTIMIZE TABLE {tabela}')

    def create_table(self, table_name, table_fields, charset='utf8mb4', engine='innodb'):
        tbl = f"CREATE TABLE IF NOT EXISTS {table_name} ( {table_fields} )DEFAULT CHARSET={charset} ENGINE={engine};"
        self.executar(tbl)
    
    def create_index(self, table_name, index_name, column_name, is_unique=False):
        u = "" if not is_unique else " UNIQUE "
        sql = f"CREATE {u} INDEX {index_name} ON {table_name} ({column_name});"
        self.executar(sql)

    def get_column_attr(self, table_name, column_name, column_attr):
        ca = column_attr.upper()
        return self.select_free(
            f'SELECT {ca} FROM information_schema.COLUMNS WHERE \
                TABLE_SCHEMA="{self.database}" AND \
                    TABLE_NAME="{table_name}" AND \
                        COLUMN_NAME="{column_name}" ')

    def get_columns_from_table(self, table_name):
        return self.select_free(
            f'SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE \
                TABLE_SCHEMA="{self.database}" AND TABLE_NAME="{table_name}" ')

    def is_number(self, x):
        # https://stackoverflow.com/questions/4187185/how-can-i-check-if-my-python-object-is-a-number
        return True if isinstance(x, (int, float, complex)) and not isinstance(x, bool) else False

    def is_bool(self, x):
        return True if isinstance(x, bool) else False

# END OF CLASS


# ####### TESTANDO A CLASSE #######

# considerações - myisam é mais rápído que innodb (em insert e update)

'''

program = 'none' # update | delete
_engine = 'MyIsam' # | InnoBD

db = Database()

if program == 'create':
    db.executar('DROP TABLE IF EXISTS teste ')
    db.create_table(
        table_name = 'teste', 
        table_fields = 'id SERIAL,  \
            nome VARCHAR(255), \
            idade INT(11), \
            vivo TINYINT(1) NOT NULL DEFAULT "1", \
            data_nascimento DATE,  \
            data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP',
        engine= _engine )

# testando optimize table
total = 1000
total_delete = total/1000

if program == 'create':
    pessoas = ('Maria', 'Jose', 'Joao', 'Amelia', 'Carlos', 'Josefina', 'Heitor', 'Gladstone')
    for i in range(1, total):
        idade_minima = 23
        idade_maxima = 80
        r = random.randint(idade_minima, idade_maxima)
        v = random.randint(0, 1)
        d = random.randint(1, 28)
        m = random.randint(1, 12)
        a = 2023 -r
        data = f'{str(a)}-{str(m)}-{str(d)}'
        nome = pessoas[random.randint(0, len(pessoas)-1)]
        db.insert(
            'teste', 
            [
                {'nome' : nome },
                {'idade' : r},
                {'vivo': v},
                {'data_nascimento': data}
            ]
        )            
    # insert - 53.0s(myisam), 4m18s(5190rows)

if program == 'update':
    for i in range(1, total):
        db.update(
            'teste',
            [
                {'nome' : f'novo fafm {i}'}
            ],
            f'id = {i}'
        )
    # update [ comment truncate table!!! ] - 52.4s(mysql), x(innodb)

if program == 'delete':
    db.delete('teste', f'id > {total_delete} ')
    # delete - 1s



result = db.select('id, nome, idade, vivo, data_nascimento', 'teste', 'id>0 limit 5')
for x in result:
    print( f'id = {x[0]} , nome = {x[1]} , idade = {x[2]} , vivo = {x[3]} , data_nascimento = {x[4]} ')

'''
