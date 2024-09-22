import pytest
import json
import sys
import os
from flask import Flask

# Ajout du chemin du répertoire parent au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app, loadClubs, loadCompetitions

# Chargement des données de test
def load_test_data():
    with open('clubs.json') as c:
        clubs = json.load(c)['clubs']
    with open('competitions.json') as comps:
        competitions = json.load(comps)['competitions']
    return clubs, competitions

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_data():
    return load_test_data()

def test_purchase_places_success(client, test_data):
    clubs, competitions = test_data

    # Simuler l'achat de places
    response = client.post('/purchasePlaces', data={
        'club': clubs[0]['name'],
        'competition': competitions[0]['name'],
        'places': 1
    })

    assert response.status_code == 200
    assert b'Great, booking complete!' in response.data
    updated_clubs = loadClubs()
    assert int(clubs[0]['points']) - 1 == int(updated_clubs[0]['points'])

def test_purchase_places_not_enough_points(client, test_data):
    clubs, competitions = test_data
    
    # Mettre à jour le club pour qu'il ait 0 points dans les données de test
    clubs[1]['points'] = '0'

    # Essayer d'acheter plus de places que de points disponibles
    response = client.post('/purchasePlaces', data={
        'club': clubs[1]['name'],  # Ce club doit avoir 0 points
        'competition': competitions[0]['name'],
        'places': 1
    })

    assert response.status_code == 200
    assert b'Not enough points available to purchase the requested number of places.' in response.data


def test_login_success(client, test_data):
    clubs, _ = test_data

    # Simuler une connexion
    response = client.post('/showSummary', data={'email': clubs[0]['email']})

    assert response.status_code == 200
    assert b'Welcome,' in response.data  # Vérifie que le message de bienvenue est présent

def test_login_failure(client):
    # Essayer de se connecter avec un email inexistant
    response = client.post('/showSummary', data={'email': 'brunell@example.com'})

    assert response.status_code == 200
    assert b'Something went wrong-please try again' in response.data
    
def test_public_club_points(client):
    response = client.get('/public_club_points')
    assert response.status_code == 200
    assert b'Public Club Points' in response.data