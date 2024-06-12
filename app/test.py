import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,  # Changez pour 3306 si nécessaire
        user='root',
        password='',  # Votre mot de passe MySQL
        database='site_promeo'
    )
    print("Connexion réussie!")
    connection.close()
except pymysql.MySQLError as e:
    print(f"Erreur de connexion à la base de données : {e}")
