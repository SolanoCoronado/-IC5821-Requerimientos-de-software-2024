from BD.client import get_db_connection

def getMyDonations(email):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC getUserDonationProjects @correoUsuario=?
                    ,@outCode=@return_code OUTPUT;
            SELECT @return_code;
            ''',
            (email)
        )

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


#pensar bien como hacer la donacion, ya que puede que haya muchos proyectos de distinto usuario con el mismo nombre 
#se podria buscar como identificar al usuario creador del proyecto para asi lograr un buen filtro (opcion)
def makeDonation(emailDonante,email,nombre_proyecto,monto,descripcion):
    try:
        #Nos conectamos a la bd
        connection = get_db_connection()
        cursor = connection.cursor()

        # Llamar al SP
        cursor.execute(
            '''
            DECLARE @return_code INT;
            EXEC createDonacion @inCorreoUsuario=?
                    ,@inCorreoProyecto=?
                    ,@inNombreProyecto=?
                    ,@inMonto=?
                    ,@inDescripcion=?
                    ,@outCode=@return_code OUTPUT;
            SELECT @return_code;
            ''',
            (emailDonante,email,nombre_proyecto,monto,descripcion)
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
    