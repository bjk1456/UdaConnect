import logging
from datetime import datetime, timedelta
from typing import Dict, List
from app import db
from app.udaconnect.models import Connection, Location,Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import time
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")


class ConnectionService:
    @staticmethod
    def createPerson(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]
        new_person.id = person["id"]

        return new_person

    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        #req = Request("http://udaconnect-persons-api.default.svc.cluster.local:5002/api/persons")
        #response = json.loads(urlopen(req).read())
        #response_data = json.loads(urlopen(req).read())
        #logger.info(f'The response is {response_data}')
        #person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}
        #person_map: Dict[str, Person] = {person.id: person for person in [ConnectionService.createPerson(r) for r in response_data]}

        result = []
        try:
            #response = requests.get("http://udaconnect-persons-api.default.svc.cluster.local:5002/api/persons")
            #response_data = response.json()
            req = Request("http://udaconnect-persons-api.default.svc.cluster.local:5002/api/persons")
            response_data = json.loads(urlopen(req).read())
            logger.info(f'The response is {response_data}')
            person_map: Dict[str, Person] = {person.id: person for person in [ConnectionService.createPerson(r) for r in response_data]}

            # Cache all users in memory for quick lookup
            #TODO replace with a REST call to persons_api's /locations endpoint
            for r in response_data:
                logger.info(f'r == {r}')
                p = ConnectionService.createPerson(r)
                logger.info(f'p.id = {p.id}')
                logger.info(f'p.last_name = {p.last_name}')


            logger.info(f'The person_map is ${person_map}')
            for k, v in person_map.items():
                logger.info(k, ":", v)


            #person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}
            #person_map: Dict[str, Person] = {person.id: person for person in response_data}
            #person_map: Dict[str, Person] = {person['id']: person for person in response_data}

            # Prepare arguments for queries
            data = []
            for location in locations:
                data.append(
                    {
                        "person_id": person_id,
                        "longitude": location.longitude,
                        "latitude": location.latitude,
                        "meters": meters,
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                    }
                )

            query = text(
                """
            SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
            FROM    location
            WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
            AND     person_id != :person_id
            AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
            AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
            """
            )
            result: List[Connection] = []
            for line in tuple(data):
                for (
                    exposed_person_id,
                    location_id,
                    exposed_lat,
                    exposed_long,
                    exposed_time,
                ) in db.engine.execute(query, **line):
                    location = Location(
                        id=location_id,
                        person_id=exposed_person_id,
                        creation_time=exposed_time,
                    )
                    location.set_wkt_with_coords(exposed_lat, exposed_long)

                    result.append(
                        Connection(
                            person=person_map[exposed_person_id], location=location,
                        )
                    )


        except HTTPError as e:
        # do something
            print('Error code: ', e.code)
        except URLError as e:
        # do something
            print('Reason: ', e.reason)
    
        return result

        
class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location
    
    @staticmethod
    def retrieve_all() -> List[Location]:
        return db.session.query(Location).all()