from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.auth.database import *
from models.user import *

router = APIRouter()


@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    return (ResponseModel(users, "Users data retrieved successfully")
            if len(users) > 0
            else ResponseModel(users, "Empty list returned")
            )


@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    return (ResponseModel(user, "User data retrieved successfully")
            if user
            else ErrorResponseModel("An error occurred.", 404, "User doesn't exist."))


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    return (ResponseModel(f"User with ID: {id} removed", "User deleted successfully")
            if deleted_user
            else ErrorResponseModel("An error occurred",
                                    404,
                                    f"User with id {id} doesn't exist")
            )


@router.put("{id}")
async def update_user(id: str, req: UpdateUserModel = Body(...)):
    updated_user = await update_user_data(id, req.dict())
    return (ResponseModel(f"User with ID: {id} name update is successful",
                          "User name updated successfully")
            if updated_user
            else ErrorResponseModel("An error occurred",
                                    404,
                                    f"There was an error updating the user {id}")
            )
