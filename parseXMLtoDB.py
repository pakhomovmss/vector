import xml.etree.ElementTree as et
from mysql.connector import Error
import mysql.connector


tree = et.parse('E:/Data Science/Datasets/EatingData/EatingData.xml')
root = tree.getroot()


def mk_rec(items, res, col1, col2):
    id_ = 1

    for val in items:
        record = {}

        record[col1] = id_
        record[col2] = val

        res.append(record)
        id_ += 1
    

def employees():
    rows = []
    names = []

    for r in range(0, len(root)):
        for name in root[r].findall('Choice'):
            emp_name = name.get('Employee')
            names.append(emp_name)
    
    names = sorted(set(names))
    
    mk_rec(names, rows, 'Id', 'Employee')

    return rows


def dishes():
    rows = []
    dishes = []

    for r in range(len(root)):
        for comp in range(3):
            for item in root[r].find('Menu')[comp].findall('Dish'):
                dishes.append(item.get('Name'))
    
    dishes = sorted(set(dishes))

    mk_rec(dishes, rows, 'Id', 'Name')

    return rows


def find_id(rows, col, name):
    for record in rows:
        if record[col] == name:
            return record['Id']


def complexes():
    rows = []

    for i in range(3):
        record = (i+1, str(i + 1) + " комплекс")
        rows.append(record)

    record = (4, "Выпечка")
    rows.append(record)
    
    return rows


def dishes_in_complex():
    rows = []
    id_ = 1

    for r in range(0, len(root)):
        for comp in range(3):
            complex_name = root[r].find('Menu')[comp].attrib.get('Name')

            for item in root[r].find('Menu')[comp].findall('Dish'):
                record = (id_, root[r].attrib.get('Date'),
                          find_id(complexes(), 'Complex', complex_name),
                          find_id(dishes(), 'Name', item.get('Name')))

                rows.append(record)
                id_ += 1

    return rows


def employee_select():
    rows = []
    id_ = 1

    emp = employees()
    cmpx = complexes()

    for r in range(len(root)):
        date = root[r].attrib.get('Date')

        for item in root[r].findall('Choice'):
            record = (id_, date, find_id(emp, 'Employee', item.get('Employee')),
                      find_id(cmpx, 'Complex', item.get('Variant')))

            rows.append(record)
            id_ += 1

    return rows


def insert(query, data):
    con = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='Pahomov2000+',
                                  db='nutritionaldb')

    try:
        cursor = con.cursor()
        cursor.executemany(query, data)

        con.commit()

        print("OK")
    
    except Error as error:
        print(error)

    finally:
        cursor.close()
        con.close()


# Load dictionaries (tables in future) into CONSTANTS

EMPLOYEES = employees()
DISHES = dishes()
COMPLEXES = complexes()

""" Добавляю строку: 1 """
#print(sorted(map(lambda x: x.lower(), ["Хлеб", "Чиввапчичи", "хлеб",  "азор"])))

# These both are the ER of three previous tables

DISHES_IN_COMPLEX = dishes_in_complex()
EMPLOYEE_SELECT = employee_select()


# Main


if __name__ == '__main__':

    #SQL queries to insert data into tables
    
    insert(data=complexes(),
           query="INSERT INTO complexes(Id, Complex) VALUES(%s, %s)")

    insert(data=DISHES_IN_COMPLEX,
           query="INSERT INTO dishesincomplex(Id, Date, CmpxId, DishId) VALUES(%s, %s, %s, %s)")
    
    insert(data=EMPLOYEE_SELECT,
           query="INSERT INTO employeeselect(Id, Date, EmpId, CmpxId) VALUES(%s, %s, %s, %s)")
