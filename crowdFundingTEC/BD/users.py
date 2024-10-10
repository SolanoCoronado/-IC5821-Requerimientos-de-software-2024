from BD.client import get_db_connection
#La primer linea importa de client.py su funcion de conexion a la bd

#Creamos funciones que van a ser llamadas por la API

def getInfoBC():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute("EXEC getDonationsDetails")

        # Obtener los resultados
        rows = cursor.fetchall()
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}

def getUsuarios():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute("EXEC obtenerUsuarios")

        # Obtener los resultados
        rows = cursor.fetchall()
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
def getByMoney():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute("EXEC getByDonation")

        # Obtener los resultados
        rows = cursor.fetchall()
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def getUser(email):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()
        # Llamar al SP
        cursor.execute('''
                    DECLARE @return_code INT;
                    EXEC getUser
                        @correo=?
                        ,@outCode=@return_code OUTPUT;
                    SELECT @return_code;
                       ''',
                       (email))
        rows = cursor.fetchall()  # fetchone() en lugar de fetchval()
        # Manejar el código de retorno
        if  isinstance(rows, int) and rows != 0:
            return {'error': "Error de email o parámetros inválidos"}

        # Obtener los resultados del SP
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}

def getUsuarioByMoney():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute("EXEC getUserByMoney")

        # Obtener los resultados
        rows = cursor.fetchall()
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}

def getByDonation():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute("EXEC getByDonation")

        # Obtener los resultados
        rows = cursor.fetchall()
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def getByDonator():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute("EXEC getByDonator")

        # Obtener los resultados
        rows = cursor.fetchall()
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def getDonations(email):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute('''
                       DECLARE @return_code INT;
                       EXEC getDonations
                       @correoUsuario=?
                       ,@outCode = @return_code OUTPUT;
                       SELECT @return_code;
                       ''',(email))

        # Obtener los resultados
        rows = cursor.fetchall()

        # Manejar el código de retorno
        if  isinstance(rows, int) and rows != 0:
            return {'error': "Error de email o parámetros inválidos"}
        resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
#hasta no tener los SP con los codigos de error sino funcionan no se va a acoplar la parte de mandar correos.  
def createUsers(nombre, apellido, contrasena, cedula, correo, cartera, telefono):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        
        cursor.execute('''
            DECLARE @return_code INT;
            EXEC createUsers
                @inNombre = ?,
                @inApellido = ?,
                @inContrasena  = ?,
                @inCedula = ?,
                @inCorreo  = ?,
                @inCartera = ?,
                @inTelefono  = ?,
                @outCode = @return_code OUTPUT;
            SELECT @return_code;
        ''',
            (nombre, apellido, contrasena, cedula, correo, cartera, telefono)
        )

        return_value = cursor.fetchval()
        
        # Cerrar el cursor y la conexión
        connection.commit() # sin esto no funciona agregar o modificar info
        cursor.close()
        connection.close()

        # Retornar los el codigo si hubo algun error
        return {"code": return_value}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {"error": str(e)}
    
def createAdmin(nombre, apellido, contrasena, cedula, correo, cartera, telefono, nameAreaTrabajo):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC createAdmin @inNombre=?
                            ,@inApellido=?
                            ,@inContrasena=?
                            ,@inCedula=?
                            ,@inCorreo=?
                            ,@inCartera=?
                            ,@inTelefono=?
                            ,@inNameAreaTrabajo=?
                            ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (nombre, apellido, contrasena, cedula, correo, cartera, telefono, nameAreaTrabajo)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()

        # Cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}


def login(correo,contrasena):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC loginStandard @inCorreo=?
                ,@inContrasena=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (correo,contrasena)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}

#de momento se queda loginAdmin, aunque parece que el otro login podria funcionar exactamente igual
def loginAdmin(correo,contrasena):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC loginAdmin @inCorreo=?
                ,@inContrasena=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (correo,contrasena)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def update(oldCorreo,nombre, apellido, contrasena, newCorreo, cartera, telefono,NA):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC updateUser @inCorreoUser=?
                        ,@newNombre=?
                        ,@newApellido=?
                        ,@newContrasena=?
                        ,@newCorreo=?
                        ,@newCartera=?
                        ,@newTelefono=?
                        ,@newAreaTrabajo=?
                        ,@outCode=@return_code OUTPUT;
            SELECT @return_code;
            ''',
            (oldCorreo,nombre,apellido,contrasena,newCorreo, cartera, telefono,NA)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()

        # Cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def updateAdmin(oldCorreo,nombre, apellido, contrasena, newCorreo, cartera, telefono, nameAreaTrabajo):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC updateUser @inCorreoUser=?
                        ,@newNombre=?
                        ,@newApellido=?
                        ,@newContrasena=?
                        ,@newCorreo=?
                        ,@newCartera=?
                        ,@newTelefono=?
                        ,@newAreaTrabajo=?
                        ,@outCode=@return_code OUTPUT;
            SELECT @return_code;
            ''',
            (oldCorreo,nombre, apellido, contrasena, newCorreo, cartera, telefono, nameAreaTrabajo)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()

        # Cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def desactivation(adminEmail,correo):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC deleteUser @inCorreoAdmin=?
                            ,@inCorreoUser=?
                            ,@outCode=@return_code OUTPUT;
            SELECT @return_code;
            ''',
            (adminEmail,correo)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()

        # Cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def agregarFondo(email,cartera):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC agregarFondos @correo=?
                            ,@monto=?
                            ,@outCode=@return_code OUTPUT;
            SELECT @return_code;
            ''',
            (email,cartera))

        # Obtener los resultados

        resultados = cursor.fetchval()

        # Cerrar el cursor y la conexión
        connection.commit()
        cursor.close()
        connection.close()

        # Retornar los resultados
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}