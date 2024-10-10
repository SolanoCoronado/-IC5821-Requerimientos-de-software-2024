from flask import Flask
import pyodbc

app = Flask(__name__)

# Configuración de la base de datos
app.config['DB_SERVER'] = 'CrowdfundingProjectsDB.mssql.somee.com'
app.config['DB_DATABASE'] = 'CrowdfundingProjectsDB'
app.config['DB_USER'] = 'AlonsoDM_SQLLogin_1'
app.config['DB_PASSWORD'] = 'lv7pherkw6'

def get_db_connection():
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={app.config["DB_SERVER"]};DATABASE={app.config["DB_DATABASE"]};UID={app.config["DB_USER"]};PWD={app.config["DB_PASSWORD"]}')
        return connection
    except pyodbc.Error as e:
        print(f'Error de conexión: {str(e)}')
        return None