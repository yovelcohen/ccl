from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from routes.user import router as UserRouter
from routes.admin import router as AdminRouter
from routes.companies import router as CompaniesRouter
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

app = FastAPI()

apm = make_apm_client()
app.add_middleware(ElasticAPM, client=apm)

token_listener = JWTBearer()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Fuck You Kenny"}


app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(UserRouter, tags=["User"], prefix="/user", dependencies=[Depends(token_listener)])
app.include_router(CompaniesRouter, tags=["Companies"], prefix="/companies")
