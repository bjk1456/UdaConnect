from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
import logging
from kafka import KafkaProducer
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")



db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.before_request
    def before_first_request():
        #TOPIC_P = 'persons'
        TOPIC_L = 'locations'
        KAFKA_SERVER = 'kafka-headless:9092'
        PARTITION = 0
        #CONSUMER_GROUP = 'udacity'
        #PERSON_CSV = '/app/udaconnect/person.csv'
        LOCATION_CSV = '/app/udaconnect/location.csv'

        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        with open(LOCATION_CSV) as f:
            for row in f:
                logger.info(f'the row is {row.strip()}')
                producer.send(topic=TOPIC_L, value=row.strip(), partition=PARTITION)
            producer.flush()
        producer.close()



    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
