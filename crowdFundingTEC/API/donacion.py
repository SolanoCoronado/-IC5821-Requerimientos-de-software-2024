from flask import Blueprint, jsonify, request
from BD.donations import *
from BD.mail import enviar_correo_gmail
donations_bp = Blueprint('donaciones', __name__)

#---------------------------GET-Donations-----------------------------------------------------------------
@donations_bp.route('/donations/<string:sesion>', methods=['GET'])
def getDonations(sesion):
    # Endpoint retorna toda donacion realizada por usuario
    resultados = getMyDonations(sesion)
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)


#---------------------------------------------------------------------------------------------------------
#--------------------------Create-Donations---------------------------------------------------------------
@donations_bp.route('/donations/donate', methods=['POST'])
def createDonation():
    # Endpoint realizar donacion
    newDonation = request.get_json()
    print(newDonation)
    resultado = makeDonation(newDonation["username"], newDonation['email']
	    , newDonation['nombreProyecto'], newDonation['monto'], newDonation['descripcion'])
    if 'error' in resultado:
        return jsonify({"message": "Error al intentar donar", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al intentar donar", "error": f"Código de error: {resultado['code']}"}), 500
    
    enviar_correo_gmail("Donación recibida", f"Su proyecto ha recibido una donación de {newDonation["monto"]}, por parte de {newDonation["email"]}.", newDonation['email'])
    enviar_correo_gmail("Gracias por su donación", f"Agradecemos su donación al proyecto {newDonation['nombreProyecto']}, con esta donación el proyecto está más cerca de su éxito.", newDonation["username"])
    return jsonify({"message": "Donacion realizada", "user": newDonation}), 201
	
#---------------------------------------------------------------------------------------------------------
#---------------------------GET-All-Donations-------------------------------------------------------------
@donations_bp.route('/donations/all/count', methods=['GET'])
def getAllDonationsCount():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM donacion;  
	    ''')
        total_donaciones = cursor.fetchval()
        cursor.close()
        connection.close()
        return jsonify({"donations_count": total_donaciones})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
