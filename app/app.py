from flask import Flask, render_template, redirect, url_for, session, request, jsonify, flash
from pony.orm import Database, Required, Optional, db_session, select
import datetime

# Configuration de l'application Flask
app = Flask(__name__)
app.secret_key = "Secret"

# Configuration de la connexion à la base de données avec Pony ORM
db = Database()

class User(db.Entity):
    nom = Required(str)
    prenom = Required(str)
    date_naissance = Required(datetime.date)
    mail = Required(str, unique=True)
    password = Required(str)
    etudiant_promeo = Required(str)
    role = Required(str)

class Rendezvous(db.Entity):
    date = Required(datetime.date)
    heure = Required(datetime.time)
    duree = Required(int)  # durée en minutes
    nom = Required(str)
    prenom = Required(str)
    mail = Required(str)
    telephone = Required(str)
    url_invitation = Optional(str, default='')

db.bind(provider='mysql', host='localhost', port=3307, user='doodle', passwd='doodle', db='site_promeo')
db.generate_mapping(create_tables=True)

@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        mail = request.form['Mail']
        password = request.form['MDP']
        print(f"Trying to login with email: {mail}")  # Ajout d'un log pour le mail saisi

        with db_session:
            user = User.get(mail=mail)
            if user and user.password == password:
                session['Mail'] = mail
                session['role'] = user.role
                if user.role == 'admin':
                    return redirect(url_for('espace_admin'))
                elif user.role == 'formateur':
                    return redirect(url_for('espace_formateur'))
                elif user.role == 'etudiant':
                    return redirect(url_for('espace_etudiant'))
                else:
                    error = "Rôle utilisateur non reconnu."
                    print(error)  # Log l'erreur de rôle non reconnu
                    return render_template('files/connexion.jinja', error=error)
            else:
                print("User not found or password mismatch")  # Log si aucun utilisateur n'est trouvé ou mot de passe incorrect
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
        date_naissance = datetime.datetime.strptime(request.form['date_naissance'], '%Y-%m-%d').date()
        mail = request.form['Mail']
        password = request.form['MDP']
        etudiant_promeo = request.form['etudiant_promeo']
        
        # Définir le rôle comme 'etudiant'
        role = 'etudiant'

        with db_session:
            User(nom=nom, prenom=prenom, date_naissance=date_naissance, mail=mail, password=password, etudiant_promeo=etudiant_promeo, role=role)
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
        with db_session:
            users = select(u for u in User)[:]
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
        
        with db_session:
            User(mail=mail, password=password, role=role, nom=nom, prenom=prenom)
            flash("Utilisateur ajouté avec succès!", "success")
        return redirect(url_for('espace_admin'))
    return render_template('files/ajouter_utilisateur.jinja')

@app.route('/ajouter_rendezvous', methods=['POST'])
def ajouter_rendezvous():
    data = request.form
    date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
    heure = datetime.datetime.strptime(data['heure'], '%H:%M').time()
    duree = int(data['duree'])
    nom = data['nom']
    prenom = data['prenom']
    mail = data['mail']
    telephone = data['telephone']
    url_invitation = data.get('url_invitation', '')

    with db_session:
        Rendezvous(date=date, heure=heure, duree=duree, nom=nom, prenom=prenom, mail=mail, telephone=telephone, url_invitation=url_invitation)
        return jsonify({'status': 'success'})

@app.route('/api/rendezvous')
def api_rendezvous():
    with db_session:
        rendezvous = select(rv for rv in Rendezvous)[:]
        events = [{'title': rv.nom, 'start': f"{rv.date}T{rv.heure}"} for rv in rendezvous]
    return jsonify(events)

@app.route('/supprimer_rendezvous', methods=['POST'])
def supprimer_rendezvous():
    try:
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        heure_debut = datetime.datetime.strptime(request.form['heure_debut'], '%H:%M').time()
        nom = request.form['nom']

        print("Date du rendez-vous à supprimer :", date)
        print("Heure de début du rendez-vous à supprimer :", heure_debut)
        print("Nom du rendez-vous à supprimer :", nom)

        with db_session:
            rv = Rendezvous.get(date=date, heure=heure_debut, nom=nom)
            if rv:
                rv.delete()
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'Rendez-vous non trouvé'})
    except Exception as e:
        print("Erreur lors de la suppression du rendez-vous :", str(e))
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
