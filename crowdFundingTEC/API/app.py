from flask import Flask, render_template
from flask_cors import CORS
from API.usuario import * 
from API.proyecto import *
from API.donacion import *
from templates import *

app = Flask(__name__,template_folder='../templates')
CORS(app, supports_credentials=True,resources={r"/*": {"origins": "*"}})  # Esto permite todas las solicitudes de todos los orígenes


app.config['SESSION_TYPE'] = 'filesystem'  # O cualquier otro backend que uses
app.config['SESSION_COOKIE_NAME'] = 'tu_cookie_de_sesion'
app.config['SESSION_COOKIE_SECURE'] = False
app.secret_key = 'tu_clave_secreta_aqui'
app.register_blueprint(donations_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(project_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def index():
    return render_template('LandingPage.html')

@app.route('/loginF')
def startLoginF():
    return render_template('Login.html')
    #return render_template('dummy.html')

@app.route('/signUpF')
def startSignUpF():
    
    return render_template('SignUp.html')
@app.route('/signUpAdminF')
def startSignUpAdmin():
    return render_template('SignUpAdmin.html')
@app.route('/start')
def startDefault():
    email = request.args.get('email')
    return render_template('start.html', username=email)
    
@app.route('/AdminPanel')
def startAdmin():
    email = request.args.get('email')
    return render_template('AdminPanel.html', username=email)

@app.route('/project')
def start2():
    email = request.args.get('username')
    return render_template('createProject.html',username=email)

@app.route('/UserManagement')
def startUserManagement():
    email = request.args.get('username')
    return render_template('AdminGestionUsers.html',username=email)

@app.route('/AdminManagementProjects')
def startProjectManagement():
    email = request.args.get('username')
    return render_template('AdminManagementProjects.html',username=email)
    
@app.route('/UserStadistic')
def startUserStadistic():
    email = request.args.get('username')
    return render_template('stadistic.html',username=email)

@app.route('/donationHistory')
def startDonationHistory():
    email = request.args.get('username')
    return render_template('donationHistory.html',username=email)

@app.route('/donationHistoryAdmin')
def startDonationHistoryAdmin():
    email = request.args.get('username')
    return render_template('donationHistoryAdmin.html',username=email)

@app.route('/myProject')
def startMyProject():
    email = request.args.get('username')
    return render_template('myProject.html',username=email)

@app.route('/availableProjects')
def startAvailableProject():
    email = request.args.get('username')
    return render_template('availableProject.html',username=email)

@app.route('/seeDetails')
def startSeeDetails():

    email = request.args.get('username')
    emailProject = request.args.get('usernameProject')
    nameProjects = request.args.get('nameProject')
    #print(emailProject)
    #print(email)
    #print(nameProjects)
    
    return render_template('seeDetails.html', username=email, usernameProject=emailProject, nameProject=nameProjects)

@app.route('/updateProject')
def startEdit():
    email = request.args.get('username')
    project_name = request.args.get('projectName')  # Obtener el nombre del proyecto desde los parámetros de la URL
    
    return render_template('updateProject.html', username=email, projectName=project_name)

@app.route('/seeDetailsAdmin')
def startSeeDetailsAd():

    email = request.args.get('username')
    emailProject = request.args.get('usernameProject')
    nameProjects = request.args.get('nameProject')

    return render_template('seeDetailsProjects.html', username=email, usernameProject=emailProject, nameProject=nameProjects)
@app.route('/updateProfile')
def startProfileEdit():
    # Obtener los parámetros de la URL
    email = request.args.get('username')

    return render_template('UserProfile.html', username=email)

@app.route('/AdminEdit')
def startProfileEditAdmin ():
    # Obtener los parámetros de la URL
    email = request.args.get('username')

    return render_template('UserProfileAdmin.html', username=email)

@app.route('/logout',methods=['GET'])
def logout():
    return render_template('Login.html')

if __name__ == "__main__":
    app.run(debug=True)