# coding=utf8

from random import choice

import flask

import psycopg2 as db
import json

app = flask.Flask(__name__)
app.debug = True

conn = db.connect("dbname='GVIS' user='postgres' host='localhost' password='postgres'")

@app.route('/')
def index():
    return flask.render_template(
        'index.html', 
        random=choice(range(1,46))
    )
    
@app.route('/ecoles')
def ecoles():
    # obtenir un curseur vers la base de données:
    cur = conn.cursor()
    # exécuter la requête SQL:
    cur.execute("""SELECT gid AS fid, label AS ecole,
                       ST_AsGeoJson(ST_Transform(geom, 4326), 7) AS geom,
                       name, ville, id, NPA
                   FROM etablissements_secondaires""")
    # et demander l'ensemble du résultat de la requête:
    ecoles = cur.fetchall()
    # créer la structure des données pour GeoJSON:
    features = []
    for row in ecoles:
        features.append({ 
            "type": "Feature", 
            "properties": { "geocode": row[0], "adresse": row[3] , "ville": row[4], "label": row[1], "id": row[5], "NPA":row[6]},
            "geometry": json.loads(row[2])
        })
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    # retourner le résultat en format JSON:
    return flask.jsonify(feature_collection)

@app.route('/population')
def population():
    # obtenir un curseur vers la base de données:
    cur = conn.cursor()
    # exécuter la requête SQL:
    cur.execute("""SELECT gid AS fid,
                       ST_AsGeoJson(ST_Transform(geom, 4326), 7) AS geom,
                       b14btot
                   FROM popwgs84""")
    # et demander l'ensemble du résultat de la requête:
    population = cur.fetchall()
    # créer la structure des données pour GeoJSON:
    features = []
    for row in population:
        features.append({ 
            "type": "Feature", 
            "properties": { "geocode": row[0], "b14btot": row[2]},
            "geometry": json.loads(row[1])
        })
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    # retourner le résultat en format JSON:
    return flask.jsonify(feature_collection)
    
@app.route('/carres')
def carres():
    # obtenir un curseur vers la base de données:
    cur = conn.cursor()
    # exécuter la requête SQL:
    cur.execute("""SELECT gid AS fid,
                       ST_AsGeoJson(ST_Transform(geom, 4326), 7) AS geom,
                       geocode, bassin, popint, dureeint
                   FROM carres""")
    # et demander l'ensemble du résultat de la requête:
    carres = cur.fetchall()
    # créer la structure des données pour GeoJSON:
    features = []
    for row in carres:
        features.append({ 
            "type": "Feature", 
            "properties": { "gid": row[0], "geocode": row[2], "bassin": row[3], "popint": row[4], "dureeint": row[5],},
            "geometry": json.loads(row[1])
        })
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    # retourner le résultat en format JSON:
    return flask.jsonify(feature_collection)

if __name__ == '__main__':
    app.run()