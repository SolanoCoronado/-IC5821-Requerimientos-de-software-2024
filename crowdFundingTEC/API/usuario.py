from flask import Blueprint, jsonify, request
from BD.users import * #reconoce carperta BD y el archivo users.py
from BD.mail import enviar_correo_gmail
from BD.proyects import *
users_bp = Blueprint('usuarios', __name__)

#---------------------------GET-USERS------------------------------------------------------------------
@users_bp.route('/user/admin/<string:email>', methods=['GET'])
def getUserByEmail(email):
    #obtiene un usuario en especifico con su email
    resultados=getUser(email)

    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500
    
    return jsonify(resultados)

@users_bp.route('/user/admin/money', methods=['GET'])
def getUserByMoney():
    #obtiene un usuario en especifico con su email
    resultados=getUsuarioByMoney()

    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500
    
    return jsonify(resultados)

@users_bp.route('/users', methods=['GET'])
def getUsers():
    # Endpoint obtener todo los usuarios
    resultados = getUsuarios()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@users_bp.route('/users/admin/donations/<string:sesion>', methods=['GET'])
def getAllDonations(sesion):
    # Endpoint obtener toda donacion
    resultados = getDonations(sesion)
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)


#-------------------------------------------------------------------------------------------------------
#---------------------------CREATE----------------------------------------------------------------------
@users_bp.route('/users', methods=['POST'])
def createUser():
    # Endpoint de creación de usuario default
    newUser = request.get_json()
    resultado = createUsers(newUser['nombre'], newUser['apellido'], newUser['contrasena'], newUser['cedula']
                            , newUser['correo'], newUser['cartera'], newUser['telefono'])
    if 'error' in resultado:
        return jsonify({"message": "Error al crear el usuario", "error": resultado["error"]}), 500
    
    # Verificar si el código de resultado es distinto de 0
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al crear el usuario", "error": f"Código de error: {resultado['code']}"}), 500
    enviar_correo_gmail("Bienvenid@ a CrowTec", "Nuestro equipo se emociona en tu incorporación a nuestra comunidad de emprendedores, inversionistas y personas que buscan oportunidades para crecer y apoyar proyectos innovadores. Nosotros creemos en el poder de las ideas y el impacto positivo que pueden tener cuando reciben el apoyo necesario.", newUser['correo']) # envia correo de bienvenida si todo sale bien
    return jsonify({"message": "Usuario creado", "user": newUser}), 201

@users_bp.route('/users/admin', methods=['POST'])
def createUserAdmin():
    # Endpoint de creación de usuario admin
    newUser = request.get_json()
    resultado = createAdmin(newUser['nombre'], newUser['apellido'], newUser['contrasena'], newUser['cedula']
                            , newUser['correo'], newUser['cartera'], newUser['telefono'], newUser['nameAreaTrabajo'])
    if 'error' in resultado:
        return jsonify({"message": "Error al crear el usuario", "error": resultado['error']}), 500
    
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al crear el usuario", "error": f"Código de error: {resultado['code']}"}), 500
    enviar_correo_gmail("Bienvenid@ a CrowTec", "Nuestro equipo se emociona en tu incorporación a nuestra comunidad de emprendedores, inversionistas y personas que buscan oportunidades para crecer y apoyar proyectos innovadores. \nNosotros creemos en el poder de las ideas y el impacto positivo que pueden tener cuando reciben el apoyo necesario.", newUser['correo']) # envia correo de bienvenida si todo sale bien
    return jsonify({"message": "Usuario administrador creado", "user": newUser}), 201

@users_bp.route('/users/addMoney', methods=['POST'])
def addMoney():
    # Endpoint de agregar fondos a un usuario
    newMonto = request.get_json()
    resultado = agregarFondo(newMonto["username"], newMonto['newCartera'])
    if 'error' in resultado:
        return jsonify({"message": "Error al agregar fondos", "error": resultado["error"]}), 500
    
    # Verificar si el código de resultado es distinto de 0
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al agregar fondos", "error": f"Código de error: {resultado['code']}"}), 500
    return jsonify({"message": "Se agregaron los fondos", "user": newMonto}), 201
#------------------------------------------------------------------------------------------------------
#---------------------------LOGIN----------------------------------------------------------------------
@users_bp.route('/users/login', methods=['POST'])
def userLogin():
    # Endpoint de verificar info login de usuario default
    user = request.get_json()
    resultado = login(user['email'],user['password'])
    if 'error' in resultado:
        return jsonify({"message": "Error al iniciar sesión", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al iniciar sesión", "error": f"Código de error: {resultado["code"]}"}), 500
    return jsonify({"message": "Login exitoso", "user": user}), 201

@users_bp.route('/users/login/admin', methods=['POST'])
def userAdminLogin():
    # Endpoint de verificar info login de usuario admin
    user = request.get_json()
    resultado = loginAdmin(user['email'],user['password'])
    if 'error' in resultado:
        return jsonify({"message": "Error al crear el usuario", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al iniciar sesión", "error": f"Código de error: {resultado['code']}"}), 500
    return jsonify({"message": "Login exitoso", "user": user}), 201
#-------------------------------------------------------------------------------------------------------
#---------------------------UPDATE----------------------------------------------------------------------
@users_bp.route('/users/update', methods=['PUT'])
def userUpdate():
    # Endpoint de editar info de usuario default
    newUserInfo = request.get_json()
    resultado = update(newUserInfo["username"],newUserInfo['newName'], newUserInfo['newApellido'], newUserInfo['newPassword']
                            , newUserInfo['newEmail'], newUserInfo['newCartera'], newUserInfo['newPhone'],"NA")
    if 'error' in resultado:
        return jsonify({"message": "Error al crear el usuario", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al modificar la información", "error": f"Código de error: {resultado['code']}"}), 500
    
    return jsonify({"message": "Informacion de usuario actualizada", "user": newUserInfo}), 201

@users_bp.route('/users/update/admin', methods=['PUT'])
def userAdminUpdate():
    # Endpoint de editar info de usuario admin
    newUserInfo = request.get_json()
    resultado = update(newUserInfo["username"],newUserInfo['newName'], newUserInfo['newApellido'], newUserInfo['newPassword']
                        , newUserInfo['newEmail'], newUserInfo['newCartera'], newUserInfo['telefono'], newUserInfo['newAreaTrabajo'])
    if 'error' in resultado:
        return jsonify({"message": "Error al modificar la información", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al modificar la información", "error": f"Código de error: {resultado['code']}"}), 500 
    return jsonify({"message": "Informacion de usuario administrador actualizada", "user": newUserInfo}), 201

@users_bp.route('/users/desactivation', methods=['DELETE'])
def userDesactivation():
    # Endpoint de desactivacion de usuario default
    user = request.get_json()
    resultado = desactivation(user["username"],user['correo'])
    if 'error' in resultado:
        return jsonify({"message": "Error al desactivar el usuario", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al desactivar el usuario", "error": f"Código de error: {resultado['code']}"}), 500 
    return jsonify({"message": "Usuario desactivado", "user": user}), 201
#-------------------------------------------------------------------------------------------------------
#---------------------------STADISTICS------------------------------------------------------------------
@users_bp.route('/users/stadistics/money', methods=['GET'])
def getProyectoByMoney():
    # Endpoint de obtener estadisticas por projectos con mayores montos recaudado
    resultados = getByMoney()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@users_bp.route('/users/stadistics/donation', methods=['GET'])
def getProyectoByDonation():
    # Endpoint de obtener estadisticas por projectos con mayores monto recibido de donaciones
    resultados = getByDonation()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@users_bp.route('/users/stadistics/donator', methods=['GET'])
def getProyectoByDonator():
    # Endpoint de obtener estadisticas por projectos con mayores donadores
    resultados = getByDonator()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@users_bp.route('/users/stadistics/burdownchart', methods=['GET'])
def getBurdownchart():
    # Endpoint de obtener estadisticas de la evolución de las donaciones de los proyectos
    resultados = getInfoBC()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)
#-------------------------------------------------------------------------------------------------------