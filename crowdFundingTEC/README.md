# prograReque
# librerias que instalar
pip install pyodbc
pip install Flask-Mail
pip install Flask

python -m API.app # iniciar a la api
http://127.0.0.1:5000/api/users # llamar a la api
# Credenciales
workstation id=CrowdfundingProjectsDB.mssql.somee.com;

packet size=4096;

user id=AlonsoDM_SQLLogin_1;

pwd=lv7pherkw6;

data source=CrowdfundingProjectsDB.mssql.somee.com;

persist security info=False;

initial catalog=CrowdfundingProjectsDB;

TrustServerCertificate=True 



Codigos de Error DB:
    50067: email ya en uso
    50068: email no válido
    50069: El monto debe ser mayor que 0
    50070: datos vacíos
    50071: Area de trabajo no encontrada
    50072: tipo de usuario no encontrado
    50075: Correo ingresado no es valido debe existir en la tabla users
    50076: Categoría no encontrada
    50078: La fecha máxima debe ser futura (Dos dias) 
    50079: Nombre de proyecto duplicado por usuario
    50080: Usuario inactivo
    50081: Credenciales incorrectas
    50082: Usuario no administrador
    50083: Usuario no standard
    50084: Fecha inválida en tipo NVARCHAR
    50085: Monto insuficiente en la cartera del usuario para donacion
    50086: Proyecto no encontrado o no pertenece al usuario
    50087: Usuario con proyectos asociados (no se puede eliminar)
    50088: Usuario no encontrado
    50089: nombre de proyecto duplicado por usuario
    50090: Correo ya existente



-- Eliminar todos los datos de la tabla
DELETE FROM users;

-- Restablecer el contador IDENTITY
DBCC CHECKIDENT ('users', RESEED, 0);
