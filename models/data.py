from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class Location(BaseModel):
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    type: Optional[str] = None


class KnownCases(BaseModel):
    prosecuters = List[str]
    defendant: str
    description: str = None
    locations: List[str] = []


class Industry(BaseModel):
    name: str
    description: str


class Company(BaseModel):
    name: str
    industries: Optional[List[Industry]] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    locations: Optional[List[Location]] = None
    known_cases: Optional[List[KnownCases]] = None
