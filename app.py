#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import api_exceptions as exc
import api_helpers as helpers
import api_schemas as schemas
from flask import Flask, g, jsonify, request
from flask_expects_json import expects_json
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker


def init_db():
    engine = create_engine("postgresql://ornitologist:ornitologist@localhost:5432/birds_db")
    db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
engine = create_engine("postgresql://ornitologist:ornitologist@localhost:5432/birds_db", echo=False)
db = scoped_session(sessionmaker(bind=engine))


@app.route('/version', methods=['GET'])
def version():
    resp = "Birds‌ ‌Service.‌ ‌Version‌ ‌0.1"
    return resp, 200


@app.route('/birds', methods=['GET'])
def api_birds():
    try:
        attr_dict = request.args
        helpers.validate_bird_select_parameters(attr_dict)
        attribute = attr_dict.get('attribute', '1')
        order = attr_dict.get('order', 'ASC')
        limit = attr_dict.get('limit', 'ALL')
        offset = attr_dict.get('offset', '0')
        resp = db.execute("""SELECT *
                           FROM birds
                           ORDER BY {} {}
                           LIMIT {}
                           OFFSET {}""".format(attribute, order, limit, offset)).fetchall()
        return jsonify([dict(r) for r in resp]), 200
    except exc.TooManyParameters as e:
        return e.description, 400
    except exc.UnexpectedParameter as e:
        return e.description, 400
    except exc.UnexpectedParameterValue as e:
        return e.description, 400


@app.route('/birds', methods=['POST'])
@expects_json(schemas.BIRD_SCHEMA, force=True)
def add_bird():
    try:
        bird_dict = g.data
        helpers.validate_no_extra_parameters(bird_dict)
        helpers.validate_bird_body_length_and_wingspan(bird_dict)
        db.execute("""INSERT INTO birds (species, name, color, body_length, wingspan)
                          VALUES (:species, :name, :color, :body_length, :wingspan)""", bird_dict)
        resp = 'Database successfully updated'
        return resp, 201
    except IntegrityError:
        return 'Bird already exist in database', 400
    except exc.BodyLengthIsNegative as e:
        return e.description, 400
    except exc.TooManyParameters as e:
        return e.description, 400
    except exc.WingspanLengthIsNegative as e:
        return e.description, 400


if __name__ == '__main__':
    app.run(debug=True, port=8080)