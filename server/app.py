#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        response_body = f"""
            <ul>ID: {animal.id}</ul>
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
        """
        return make_response(response_body, 200)
    else:
        return make_response("Animal not found", 404)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        animal_names_html = ""
        for animal in zookeeper.animals:
            animal_names_html += f"<ul>Animal: {animal.name}</ul>"

        response_body = f"""
            <ul>ID: {zookeeper.id}</ul>
            <ul>Name: {zookeeper.name}</ul>
            <ul>Birthday: {zookeeper.birthday}</ul>
            {animal_names_html}
        """
        return make_response(response_body, 200)
    else:
        return make_response("Zookeeper not found", 404)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        animal_names_html = ""
        for animal in enclosure.animals:
            animal_names_html += f"<ul>Animal: {animal.name}</ul>"

        response_body = f"""
            <ul>ID: {enclosure.id}</ul>
            <ul>Environment: {enclosure.environment}</ul>
            <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
            {animal_names_html}
        """
        return make_response(response_body, 200)
    else:
        return make_response("Enclosure not found", 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
