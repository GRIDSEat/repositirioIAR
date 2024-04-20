"""
Script adaptado para base de datos del IAR
Fuente: https://github.com/sungkhum/MicroPyDatabase
Fecha: 28/10/2023
"""
import json
import lib.micropydatabase.micropydatabase as mdb

def creaBD():
    try:
        mdb.Database.create("iarDB",200)
    except Exception:
        return 'Error.'
    else:
        return 'Success.'

def creaTabla():
    try:
        db_object = mdb.Database.open("iarDB")
        db_object.create_table("usuario", {"idUsuario":int, "apellido":str, "electronica":int,"anecoica":int,"mecanica":int,"salaLimpia":int,"faraday":int})
        db_object.create_table("instrumento", {"idInstrumental":int, "nombre":str, "electronica":int,"anecoica":int,"mecanica":int,"salaLimpia":int,"faraday":int})
    except Exception:
        return 'Error.'
    else:
        return 'Success.'
#-----------------------------------------------------------------------------------------------------------

def alta(dato,tabla):
    if tabla=="usuario":
        db_object = mdb.Database.open("iarDB")
        dbUsuario = db_object.open_table("usuario")
        datoParseado = json.loads(dato)
        dbUsuario.insert(datoParseado)
    elif tabla=="instrumento":
        db_object = mdb.Database.open("iarDB")
        dbInstrumento = db_object.open_table("instrumento")
        datoParseado = json.loads(dato)
        dbInstrumento.insert(datoParseado)


#Update actualiza filas previamente definidas 
def test_update_row():
    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        db_table.update_row(4, {"nombre": "Maria", "id": "2c","permiso":13})
    except Exception:
        return 'Error.'
    else:
        return 'Success.'

#Actualiza la fila especificada por otra
def test_update():

    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        db_table.update({"nombre": "Esteban", "id": "5c","permiso":16},
                        {"nombre": "Horacio", "id": "87h","permiso":43})    
    except Exception:
        return 'Error.'
    else:
        return 'Success.'

#Borra fila 5
def test_delete_row():
    try:
        db_object = mdb.Database.open("iarDB")
        db_table = db_object.open_table("tablainstrumento")
        
        db_table.delete_row(5)
    except Exception:
        return 'Error.'
    else:
        return 'Success.'


#Consulta una fila predeterminada
def test_find_row():
    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        salida = db_table.find_row(2)
        print(salida)
    except Exception:
        return 'Error.'
    else:
        return 'Success.'

#Cuenta cuantas filas son coincidentes
def test_query():
    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        db_table.update_row(4, {"nombre": "Fabiana", "id": "20c", "permiso": 500})
        db_table.insert({"nombre": "Fabiana", "id": "20c", "permiso": 500})
        db_table.insert({"nombre": "mario", "id": "1c","permiso":12})
        return_list = db_table.query({"nombre": "Fabiana", "id": "20c", "permiso": 500})
        
    except Exception:
        return 'Error.'
    if len(return_list) >= 2:
        print(len(return_list))
        return 'Success.'
    else:
        return 'Error.'

#Si encuentra los datos correctos en alguna fila devuelve Success
def test_find():
    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        db_table.find({"nombre": "mario", "id": "1c","permiso":12})
    except Exception:
        return 'Error.'
    else:
        return 'Success.'

#Busca en las filas una coincidecia de un dato perteneciente a un campo
def test_scan_no_query():
    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        scan_return = db_table.scan()
        the_scan = scan_return.__next__()

    except Exception:
        return 'Error.'
    if the_scan['nombre'] == 'mario':
        return 'Success.'
    else:
        return 'Error.'
#----------------------------------------------------------------------------------------------------------------
#Genial!!! busca en la tabla una coincidencia de uno de los campos teniendo como referencia a otro campo
#----------------------------------------------------------------------------------------------------------------
def test_scan_with_query():
    try:
        db_object = mdb.Database.open("iarDB")
        db_table = db_object.open_table("tablainstrumento")
        scan_return = db_table.scan({"id":"4d"})
        the_scan = scan_return.__next__()
        if the_scan['id'] == '4d':
            print ("Dato encontrado en instrumentos")
        return 'Success.'
    except Exception:
        try:
            db_table = db_object.open_table("tablaempleado")
            scan_return = db_table.scan({"id":"4d"})
            the_scan = scan_return.__next__()
            if the_scan["id"]=="4d":
                print("Dato encontrado en empleados")
            return "Success."
        except Exception:
            return 'Error'

#Cuenta cantidad de filas total de la tabla
def check_current_row():
    try:
        db_object = mdb.Database.open("testdb")
        db_table = db_object.open_table("testtable")
        current_row = db_table.__calculate_current_row()
    except Exception:
        return 'Error.'
    if int(current_row) == 16:
        return 'Success.'
    else:
        return 'Error.'
 
#borra todos los elementos de la tabla
def test_truncate():
    try:
        db_object = mdb.Database.open("iarDB")
        db_table = db_object.open_table("tablainstrumento")
        db_table.truncate()
    except Exception:
        return 'Error.'
    for file_name in mdb.os.listdir('iarDB/tablainstrumento'):
        if file_name[0:1] == 'data':
            return 'Error.'
    else:
        return 'Success.'




# Clean up all the test data
def borra_DB():
    
    try:
        for file_name in mdb.os.listdir('iarDB/tablaempleado'):
            mdb.os.remove('iarDB/tablaempleado/' + file_name)
        mdb.os.rmdir('iarDB/tablaempleado')
        for file_name in mdb.os.listdir('iarDB'):
            mdb.os.remove('iarDB/' + file_name)
        mdb.os.rmdir('iarDB')
    except Exception:
        return 'Failed to delete test data.'
    
    try:
        for file_name in mdb.os.listdir('iarDB/tablainstrumento'):
            mdb.os.remove('iarDB/tablainstrumento/' + file_name)
        mdb.os.rmdir('iarDB/tablainstrumento')
        for file_name in mdb.os.listdir('iarDB'):
            mdb.os.remove('iarDB/' + file_name)
        mdb.os.rmdir('iarDB')
    except Exception:
        return 'Failed to delete test data.'
    


print("Testing started")

print("------")

assert creaBD() == "Success.", "Error: Create database"

assert creaTabla() == "Success.", "Error: Create table"

"""
assert alta() == "Success.", "Error: Alta"

assert test_update_row() == "Success.", "Error: Update row"

assert test_update() == "Success.", "Error: Update"

assert test_delete_row() == "Success.", "Error: Delete row"

assert test_find_row() == "Success.", "Error: Find row"

assert test_query() == "Success.", "Error: Query exception"

assert test_find() == "Success.", "Error: Find exception"

assert test_scan_no_query() == "Success.", "Error: Scan without query"

assert test_scan_with_query() == "Success.", "Error: Dato no encontrado"

assert check_current_row() == "Success.","Error: Current row error"

assert test_truncate() == "Success.", "Error: Truncate"


borra_DB()
"""



print("------")
print("All tests passed.")
