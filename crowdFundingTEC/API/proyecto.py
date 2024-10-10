from flask import Blueprint, jsonify, request
from BD.proyects import *
from BD.mail import enviar_correo_gmail
import base64
project_bp = Blueprint('projectos', __name__)

#---------------------------GET-Projects------------------------------------------------------------------
@project_bp.route('/projects', methods=['GET'])
def getProjects():
    # Enpoint retorna todos los proyectos de mayor a menor exitoso
    resultados = getAllProjects()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)
@project_bp.route('/projects/users', methods=['GET'])
def getUsersProjects():
    # Endpoint de extraer todos los proyectos
    # pero ordenados por nombre de usuario
    resultados = getProyectosByUserName()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@project_bp.route('/projects/user/<string:sesion>', methods=['GET'])
def geProjectByEmail(sesion):
    # Endpoint de extraer los proyectos unicamente del usuario que lo solicita
    resultados = getProyectByUser(sesion)
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@project_bp.route('/projects/user/donations', methods=['GET'])
def getUserDonationProjects():
    # Endpoint de extraer los proyectos a los que se ha donaddo
    resultados = getProyectosByUserDonation()
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

@project_bp.route('/projects/user/<string:nombre>/<string:sesion>', methods=['GET'])
def getUserProject(nombre,sesion):
    # Endpoint de extraer el proyecto por nombre
    resultados = getProyecto(nombre,sesion)
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)


@project_bp.route('/projects/user/project/<string:nombre>/<string:sesion>', methods=['GET'])
def getUserProjecto(nombre,sesion):
    # Endpoint de extraer la info detallada de 1 proyecto de 1 usuario
    resultados = getProyect(nombre,sesion)
    
    # Verificar si hubo un error
    if isinstance(resultados, dict) and 'error' in resultados:
        return jsonify(resultados), 500  # Retornar error con código 500

    # Retornar los resultados en formato JSON
    return jsonify(resultados)

# Endpoint para extraer imágenes
@project_bp.route('/images/<string:userEmail>/<string:projectName>', methods=['GET'])
def get_images(userEmail,projectName):
    try:
        images = fetch_images_from_db(userEmail, projectName)
        # Convertir los bytes de las imágenes a base64 para enviarlas al frontend
        base64_images = [base64.b64encode(image).decode('utf-8') for image in images]
        return jsonify(base64_images), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
# Endpoint para extraer urls videos
@project_bp.route('/video/<string:userEmail>/<string:projectName>', methods=['GET'])
def get_videos(userEmail,projectName):
    try:
        videos = fetch_videos_from_db(userEmail, projectName)
        # Convertir los bytes de las imágenes a base64 para enviarlas al frontend
        if isinstance(videos, dict) and 'error' in videos:
            return jsonify(videos), 500  # Retornar error con código 500
        return jsonify(videos), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
#---------------------------------------------------------------------------------------------------------
#--------------------------Create-Projects----------------------------------------------------------------
@project_bp.route('/project', methods=['POST'])
def createProject():
    # Endpoint creacion de proyecto
    newProject = request.get_json()
    resultado = createProyecto(newProject['nombre'],newProject['descripcion']
        ,newProject['objetivo'],newProject['monto'] ,newProject['max_date']
        ,newProject['nameCategoria'],newProject['userEmail'])
    if 'error' in resultado:
        return jsonify({"message": "Error al crear el proyecto", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al crear el proyecto", "error": f"Código de error: {resultado['code']}"}), 500
    return jsonify({"message": "Proyecto creado", "user": newProject}), 201

@project_bp.route('/upload/<string:userEmail>/<string:projectName>', methods=['POST'])
def upload_image(userEmail,projectName):
    #endpoint que guarda una img en la BD
    if 'image' not in request.files:
        return jsonify({"message": "No image provided"}), 400


    file = request.files['image']
    image_bytes = file.read()  # Leer la imagen como bytes

    try:
        # Guardar la imagen en la base de datos
        save_image_to_db(userEmail,projectName,image_bytes)
        return jsonify({"message": "Image uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
@project_bp.route('/upload/video', methods=['POST'])
def upload_video():
    #endpoint que guarda el url de un video en la BD
    try:
        newVideo= request.get_json()
        save_video_to_db(newVideo["emailUser"],newVideo["nameProject"],newVideo["enlace"])
        return jsonify({"message": "Video uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
#---------------------------------------------------------------------------------------------------------
#--------------------------Update-Projects----------------------------------------------------------------
@project_bp.route('/project/update', methods=['PUT'])
def updateProject():
    # Endpoin modificacion de proyecto
    newProjectInfo = request.get_json()
    resultado = updateProyecto(newProjectInfo['oldProyectName'],newProjectInfo["userEmail"],newProjectInfo["newName"]
        ,newProjectInfo['newDescripcion']
        ,newProjectInfo['newObjetivo'],newProjectInfo['newMonto'] ,newProjectInfo['newMaxDate']
        ,newProjectInfo['newCategoria'])
    if 'error' in resultado:
        return jsonify({"message": "Error al editar el proyecto", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al editar el proyecto", "error": f"Código de error: {resultado['code']}"}), 500
    enviar_correo_gmail("Actualización de proyecto", f"Su proyecto {newProjectInfo['oldProyectName']} ha sido modificado.", newProjectInfo["userEmail"]) # envia correo de bienvenida si todo sale bien
    return jsonify({"message": "Proyecto editado", "user": newProjectInfo}), 201
#---------------------------------------------------------------------------------------------------------
@project_bp.route('/project/delete', methods=['DELETE'])
def deleteProject():
    # Endpoin modificacion de proyecto
    projectInfo = request.get_json()
    resultado = deleteProyecto(projectInfo["username"],projectInfo['email'],projectInfo["nombre"])
    if 'error' in resultado:
        return jsonify({"message": "Error al eliminar el proyecto", "error": resultado['error']}), 500
    if 'code' in resultado and resultado["code"] != 0:
        return jsonify({"message": "Error al eliminar el proyecto", "error": f"Código de error: {resultado['code']}"}), 500

    return jsonify({"message": "Proyecto eliminado", "user": projectInfo}), 201