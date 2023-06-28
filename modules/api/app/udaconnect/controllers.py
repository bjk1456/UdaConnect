from datetime import datetime
import logging

from app.udaconnect.models import Connection, Location
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema
)
from app.udaconnect.services import ConnectionService, LocationService
from app.udaconnect.consumer import ConsumerPersons
from app.udaconnect.producer import ProducePersons
from app.udaconnect.consumer_copy import ConsumerLocations

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")


# TODO: This needs better exception handling


@api.route("/locations")
class LocationsResource(Resource):
    @responds(schema=LocationSchema, many=True)
    def get(self) -> List[Location]:
        locations: List[Location] = LocationService.retrieve_all()
        logger.info("Inside API controllers.py ... locations are:")
        for l in locations:
            logger.info(l.id)
        logger.info("|||||||||||||||||||||||||")
        logger.info("About to get ConsumerPersons.get_all_persons")
        print("OK")

        #logger.info("About to produce persons")
        #ProducePersons.produce_persons()

        #locationz: List[Location] = ConsumerPersons.get_all_persons()
        locationz: List[Location] = ConsumerLocations.get_all_locations()
        for z in locationz:
            logger.info('The ConsumerLocations are ... ')
            logger.info(z['id'])
            logger.info(z['longitude'])
        return locations
    

    
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
                                                                                                                                                                                                                                                                                     
@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
