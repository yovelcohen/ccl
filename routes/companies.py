from typing import Optional

from fastapi import APIRouter, status, HTTPException

from api_utils import get_object_or_404
from common.consts import LOCATIONS
from database.cybele.companies import companies_collection, industries_collection
from models.data import Company
from routes.utils.auth import is_authenticated
from routes.utils.upsert_data import BaseUploaderFromAPI, missing_param_exception

router = APIRouter()


class CompanyUploaderFromAPI(BaseUploaderFromAPI):
    collection = companies_collection
    id_field = 'company_id'
    allowed_data_types = [LOCATIONS]

    def serialize_input_for_upsert(self) -> dict:
        return {
            'name': self.initial_data.get('name'),
            'industry': self.initial_data.get('industry'),
            'website': self.initial_data.get('website'),
        }


@router.post("/", response_description="Upload Company", status_code=status.HTTP_201_CREATED)
@is_authenticated
async def create_company(company: Company):
    if not company.name:
        raise missing_param_exception('name')
    company_id = await CompanyUploaderFromAPI(new=True, data=company.dict()).upload()
    return {'company_id': company_id}


@router.put("/{company_id}", status_code=status.HTTP_200_OK)
@is_authenticated
async def update_company(company_id, data: Company):
    company = await get_object_or_404(companies_collection, company_id)
    company_id = await CompanyUploaderFromAPI(new=False, data=data.dict(), obj_id=company.get('_id')).upload()
    return {'company_id': company_id}


@router.get("/search}", status_code=status.HTTP_200_OK)
async def search_company(company_name: Optional[str] = None, company_id: Optional[str] = None):
    if not company_id and not company_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='you must provide either the company_name or company id params')

    company = await get_object_or_404(companies_collection, company_name)
    company_industries = industries_collection.find({"_id": {"$in": company.industries}})

    # TODO: THIS IS WHERE THE GRAPH WILL COME IN, MONGO FOR NOW
    industries_traces = ''
    company_tags_traces = ''
