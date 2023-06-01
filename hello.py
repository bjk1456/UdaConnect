
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from flask_sqlalchemy import SQLAlchemy
from typing import Dict

print("Hello")

class Person():
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)


req = Request("http://localhost:30002/api/persons")
response = {}
try:
    response = json.loads(urlopen(req).read())
     # Cache all users in memory for quick lookup
    person_map: Dict[str, Person] = {response['id']: response for response in response}
    print(person_map)
    for p in response:
        print(p['id'])
    print(f'the response is ${response}')
except HTTPError as e:
        # do something
    print('Error code: ', e.code)
except URLError as e:
        # do something
    print('Reason: ', e.reason)

print(f'the response is ${response}')
            
