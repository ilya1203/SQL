import sqlite3


class SQLwriter:

    def __init__(self):
        self.name = 'db'
        self.table = ''

    def create_column(self, columns):
        db = sqlite3.connect(f'{self.name}.sqlite')
        cursor = db.cursor()
        try:
            cursor.executescript(f"""
                    CREATE TABLE {self.table}(
                        pk int
                    );""")
            db.commit()
        except Exception as ex:
            pass

        for column in columns:
            try:
                cursor.executescript(f"""
                    ALTER TABLE {self.table}
                    ADD {column['name']} {column['type']};
                """)
            except Exception as ex:
                pass
        else:
            db.commit()
        db.close()

    def get_pk(self):
        if(len(SQLwriter.get_value(self=self))>0):
            db = sqlite3.connect(f'{self.name}.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT pk FROM {self.__class__.__name__}")
            result = cursor.fetchall()
            print(str(result[-1]).split(',')[0].split('(')[-1])
            db.close()
            return int(str(result[-1]).split(',')[0].split('(')[-1])
        else:
            return 0

    def get_value(self):
        db = sqlite3.connect(f'{self.name}.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM {self.__class__.__name__}")
        result = cursor.fetchall()
        db.close()
        return result

    def set_value(self, values):
        db = sqlite3.connect(f'{self.name}.sqlite')
        cursor = db.cursor()
        comand = f"INSERT INTO {self.__class__.__name__} VALUES {values};"
        print(comand)
        cursor.execute(comand)
        db.commit()
        db.close()

class ModelsSql:

    def __init__(self):
        self.mkdb()
        self.name = 'db'

    def create_obj(self, args):
        name = self.__class__.__name__
        print(f"created into {name} {args}")
        pk = SQLwriter.get_pk(self=self) + 1
        val = f'({pk}'
        for v in args:
            if type(v) == type(str()):
                val = f'{val}, "{v}"'
            else:
                val = val + ',' + str(v)
        else:
            val = val + ')'
        SQLwriter.set_value(self=self, values=val)

    def view(self):

        area = []
        for key in self.__class__.__dict__.keys():
            if key != '__module__' and key != '__doc__':
                area.append(key)

        to_return = []
        counter = 0
        for element in SQLwriter.get_value(self=self):
            to_return.append({})
            for i in range(len(element)):
                if i == 0:
                    to_return[counter]['pk'] = (element[i])
                else:
                    for ar in range(len(area)):
                        if i == ar+1:
                            to_return[counter][area[ar]] = (element[i])
            else:
                counter += 1
        return to_return

    def sord(self, by):
        val = self.view()
        to_return = []
        for element in val:
            for key in by.keys():
                if element[key] == by[key]:
                    to_return.append(element)
        return to_return

    def OrmInteger(self=None):
        return 'int'
    def OrmFloat(self=None):
        return 'real'
    def OrmText(self=None,mx=255):
        return f'varchar({mx})'

    def mkdb(self):
        nm = self.__class__.__name__
        print(nm)
        area=[]
        for key in self.__class__.__dict__.keys():
            if key != '__module__' and key != '__doc__':
                print(f"{key}-{self.__class__.__dict__[key]}")
                area.append({"name": key, "type": self.__class__.__dict__[key]})
        else:
            sc = SQLwriter()
            sc.table = nm
            sc.create_column(columns=area)

class TraTra(ModelsSql):
    a = ModelsSql.OrmInteger()
    b = ModelsSql.OrmText(mx=122)


