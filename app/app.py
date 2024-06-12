from flask import Flask, render_template, redirect, url_for, session, request, jsonify, flash
import pymysql
# import bcrypt  # Commenté car nous n'utilisons pas le hachage pour les tests

# Configuration de la connexion à la base de données MySQL
app = Flask(__name__)
app.secret_key = "Secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306  # Assurez-vous que c'est le bon port
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Assurez-vous que c'est le bon mot de passe
app.config['MYSQL_DB'] = 'site_promeo'

def connect_db():
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        mail = request.form['Mail']
        password = request.form['MDP']
        print(f"Trying to login with email: {mail}")  # Ajout d'un log pour le mail saisi
        user = get_user(mail)
        if user:
            print(f"User found: {user}")  # Log les détails de l'utilisateur trouvé
            # Direct password comparison without hashing
            if password == user['MDP']:
                session['Mail'] = mail
                session['role'] = user['role']
                if user['role'] == 'admin':
                    return redirect(url_for('espace_admin'))
                elif user['role'] == 'formateur':
                    return redirect(url_for('espace_formateur'))
                elif user['role'] == 'etudiant':
                    return redirect(url_for('espace_etudiant'))
                else:
                    error = "Rôle utilisateur non reconnu."
                    print(error)  # Log l'erreur de rôle non reconnu
                    return render_template('files/connexion.jinja', error=error)
            else:
                print("Password mismatch")  # Log si le mot de passe ne correspond pas
        else:
            print("User not found")  # Log si aucun utilisateur n'est trouvé
        error = "Identifiant ou mot de passe incorrect."
        return render_template('files/connexion.jinja', error=error)
    else:
        if 'role' in session:
            if session['role'] == 'admin':
                return redirect(url_for('espace_admin'))
            elif session['role'] == 'formateur':
                return redirect(url_for('espace_formateur'))
            elif session['role'] == 'etudiant':
                return redirect(url_for('espace_etudiant'))
        return render_template('files/connexion.jinja')
    
@app.route('/deconnexion')
def deconnexion():
    session.clear()  # Efface toutes les données de session
    return redirect(url_for('index'))  # Redirige vers la page d'accueil


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        mail = request.form['Mail']
        password = request.form['MDP']
        etudiant_promeo = request.form['etudiant_promeo']
        
        # Définir le rôle comme 'etudiant'
        role = 'etudiant'

        # Direct password storage without hashing
        hashed_password = password

        db = connect_db()
        if db is None:
            flash("Erreur de connexion à la base de données. Veuillez réessayer plus tard.", "danger")
            return render_template('files/inscription.jinja')

        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (nom, prenom, date_naissance, Mail, MDP, etudiant_promeo, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nom, prenom, date_naissance, mail, hashed_password, etudiant_promeo, role)
        )
        db.commit()
        cur.close()
        db.close()
        flash("Inscription réussie! Veuillez vous connecter.", "success")
        return redirect(url_for('connexion'))
    return render_template('files/inscription.jinja')

@app.route('/espace_etudiant')
def espace_etudiant():
    if 'role' in session and session['role'] == 'etudiant':
        return render_template('files/espace_etudiant.jinja')
    else:
        return redirect(url_for('connexion'))

@app.route('/espace_formateur')
def espace_formateur():
    if 'role' in session and session['role'] == 'formateur':
        return render_template('files/espace_formateur.jinja')
    else:
        return redirect(url_for('connexion'))

@app.route('/espace_admin')
def espace_admin():
    if 'role' in session and session['role'] == 'admin':
        users = get_all_users()
        return render_template('files/espace_admin.jinja', users=users)
    else:
        return redirect(url_for('connexion'))

@app.route('/ajouter_utilisateur', methods=['GET', 'POST'])
def ajouter_utilisateur():
    if request.method == 'POST':
        mail = request.form['Mail']
        password = request.form['MDP']
        role = request.form['role']
        nom = request.form['nom']
        prenom = request.form['prenom']
        add_user(mail, password, role, nom, prenom)
        flash("Utilisateur ajouté avec succès!", "success")
        return redirect(url_for('espace_admin'))
    return render_template('files/ajouter_utilisateur.jinja')

@app.route('/ajouter_rendezvous', methods=['POST'])
def ajouter_rendezvous():
    data = request.form
    date = data['date']
    heure = data['heure']
    duree = data['duree']
    nom = data['nom']
    prenom = data['prenom']
    mail = data['mail']
    telephone = data['telephone']
    url_invitation = data.get('url_invitation', '')

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO rdvs (Date, Heure, Duree, Nom, Prenom, Mail, Telephone, Url_invitation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (date, heure, duree, nom, prenom, mail, telephone, url_invitation)
    )
    db.commit()
    db.close()

    return jsonify({'status': 'success'})

@app.route('/api/rendezvous')
def api_rendezvous():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT Date, Heure, Nom FROM rdvs")
    rendezvous = cursor.fetchall()
    db.close()

    events = []
    for rv in rendezvous:
        events.append({
            'title': rv['Nom'],
            'start': f"{rv['Date']}T{rv['Heure']}"
        })

    return jsonify(events)

@app.route('/supprimer_rendezvous', methods=['POST'])
def supprimer_rendezvous():
    try:
        rdv_id = request.form['id']
        print("ID du rendez-vous à supprimer :", rdv_id)  # Correction du débogage
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM rdvs WHERE id = %s", (rdv_id,))
        db.commit()
        db.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Erreur lors de la suppression du rendez-vous :", str(e))
        return jsonify({'status': 'error', 'message': str(e)})

def get_user(mail):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE Mail = %s", (mail,))
    user = cursor.fetchone()
    db.close()
    return user

def get_all_users():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    db.close()
    return users

def add_user(mail, password, role, nom, prenom):
    # Direct password storage without hashing
    hashed_password = password
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (Mail, MDP, role, nom, prenom) VALUES (%s, %s, %s, %s, %s)",
        (mail, hashed_password, role, nom, prenom)
    )
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run(debug=True)
