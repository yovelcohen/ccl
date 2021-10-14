from fastapi import APIRouter, Request

from api_utils.handlers.location import LocationsHandler
from database.cybele.collections import locations

router = APIRouter()


@router.post("/location")
def create(request: Request):
    handler = LocationsHandler(request=request)


def search(request: Request, q):
    search_results = yield locations.command({"find": "locations",
                                             "filter": {"$text": {"$search": "dogs"}}})
