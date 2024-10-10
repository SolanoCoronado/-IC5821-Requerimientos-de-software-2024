from BD.client import get_db_connection
import pyodbc
#La primer linea importa de client.py su funcion de conexion a la bd

#Creamos funciones que van a ser llamadas por la API
def getAllProjects():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute('EXEC getAllProjects')

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
    
def getProyectosByUserName():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute('EXEC getProjectsByUser')

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
    
def getProyectByUser(email):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute('''
                       DECLARE @return_code INT;
                       EXEC getProject
                       @correoUsuario=?
                       ,@outCode=@return_code;
                       SELECT @return_code;
                       ''',(email))

        # Obtener los resultados
        rows = cursor.fetchall()
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
    
def fetch_images_from_db(email, proyectName):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute('''
                       DECLARE @return_code INT;
                       EXEC getImagenesByProyecto
                       @inCorreoUsuario=?
                       ,@inNombreProyecto=?
                       ,@outCode=@return_code;
                       SELECT @return_code;
                       ''',(email,proyectName))
        
        # Obtener los resultados
        rows = cursor.fetchall()
        if  isinstance(rows, int) and rows != 0:
            return {'error': "Error de email o parámetros inválidos"}
        
        resultados = [row[0] for row in rows]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    
def fetch_videos_from_db(email, proyectName):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP

        cursor.execute('''
                       DECLARE @return_code INT;
                       EXEC getVideosByProyecto
                       @inCorreoUsuario=?
                       ,@inNombreProyecto=?
                       ,@outCode=@return_code;
                       SELECT @return_code;
                       ''',(email,proyectName))


        # Obtener los resultados
        rows = cursor.fetchall()
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
    
def getProyectosByUserDonation():
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute('EXEC getProjectsByUserDonation')

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
    
def getProyecto(nombre,email):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()
        # Llamar al SP
        cursor.execute('''
                    DECLARE @return_code INT;
                    EXEC getProyecto
                        @nombreProyecto=?
                        ,@correoUsuario=?
                        ,@outCode=@return_code OUTPUT;
                    SELECT @return_code;
                       ''',
                       (nombre,email))
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
    
def getProyect(nombre,email):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()
        # Llamar al SP
        cursor.execute('''
                    DECLARE @return_code INT;
                    EXEC getUserProject
                        @correoUsuario=?
                        ,@nombreProyecto=?
                        ,@outCode=@return_code OUTPUT;
                    SELECT @return_code;
                       ''',
                       (email,nombre))
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
#################################################################################################
#Atenue a cambios por modo de manejar la media.
def createProyecto(nombre, descripcion, objetivo, monto, max_date, nameCategoria, userEmail):
    try:
        # Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP con parámetros
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC createProyecto @inNombreProyecto=?
                ,@inDescripcion=?
                ,@inObjetivo=?
                ,@inMonto=?
                ,@inMaxDate=?
                ,@inCorreo=?
                ,@inCategoria=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (nombre, descripcion, objetivo, monto, max_date,userEmail,nameCategoria)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()
        connection.commit()
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def save_image_to_db(email,projectName,image):
    try:
        # Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP con parámetros
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC createImagen @inCorreoUsuario=?
                ,@inNombreProyecto=?
                ,@inImagen=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (email,projectName,pyodbc.Binary(image))
        )

        # Obtener los resultados
        resultados = cursor.fetchval()
        connection.commit()
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def save_video_to_db(email,projectName,enlace):
    try:
        # Nos conectamos a la bd
        print(email,projectName,enlace)
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP con parámetros
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC createVideo @inCorreoUsuario=?
                ,@inNombreProyecto=?
                ,@inVideoURL=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (email,projectName,enlace)
        )

        # Obtener los resultados

        resultados = cursor.fetchval()

        connection.commit()
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def updateProyecto(oldNombre,email,newName,descripcion, objetivo, monto, max_date, nameCategoria):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC updateProject 
                @inNombreProyecto=?
                ,@inCorreoCreador=?
                ,@newNombre=?
                ,@newDescripcion=?
                ,@newObjetivo=?
                ,@newMonto=?
                ,@newMaxDate=?
                ,@newCategoria=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (oldNombre,email,newName,descripcion, objetivo, monto, max_date, nameCategoria)
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
    
def deleteProyecto(adminEmail,email,nombreProyecto):
    try:
        # Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP con parámetros
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC deleteProject @inCorreoAdmin=?
                ,@inCorreoProyecto=?
                ,@inNombreProyecto=?
                ,@outCode = @return_code OUTPUT;
            SELECT @return_code;
            ''',
            (adminEmail, email, nombreProyecto)
        )

        # Obtener los resultados
        resultados = cursor.fetchval()
        connection.commit()
        return {"code": resultados}
    except Exception as e:
        # Manejar el error y retornar algo significativo para la API
        return {'error': str(e)}
    finally:
        # Asegurarse de cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if connection:
            connection.close()