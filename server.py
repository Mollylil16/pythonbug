import json
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

def saveCompetitions(competitions):
    with open('competitions.json', 'w') as comps:
        json.dump({"competitions": competitions}, comps, indent=4)

def saveClubs(clubs):
    with open('clubs.json', 'w') as c:
        json.dump({"clubs": clubs}, c, indent=4)

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    club = [club for club in clubs if club['email'] == email]

    if not club:
        flash("Something went wrong-please try again")
        return render_template('index.html')  # Ou une page d'erreur

    club = club[0]
    return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > int(club['points']):
        fflash("Not enough points available to purchase the requested number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > int(competition['numberOfPlaces']):
        flash("Not enough places available in the competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > 12:
        flash("You cannot book more than 12 places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Mise à jour des points et des places
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = str(int(club['points']) - placesRequired)  # Convertir les points en str pour la sauvegarde

    # Sauvegarde des compétitions et des clubs après mise à jour
    saveCompetitions(competitions)
    saveClubs(clubs)  # Ajouté ici

    flash('Great, booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
