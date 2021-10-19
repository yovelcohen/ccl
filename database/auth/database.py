from bson import ObjectId

from .database_helper import user_helper, admin_helper
from .collections import admin_collection, user_collection


async def add_admin(admin_data: dict) -> dict:
    admin = await admin_collection.insert_one(admin_data)
    new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)


async def retrieve_users():
    students = []
    async for user in user_collection.find():
        students.append(user_helper(user))
    return students


async def add_user(student_data: dict) -> dict:
    student = await user_collection.insert_one(student_data)
    new_student = await user_collection.find_one({"_id": student.inserted_id})
    return user_helper(new_student)


async def retrieve_user(id: str) -> dict:
    student = await user_collection.find_one({"_id": ObjectId(id)})
    if student:
        return user_helper(student)


async def delete_user(id: str):
    student = await user_collection.find_one({"_id": ObjectId(id)})
    if student:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_user_data(id: str, data: dict):
    student = await user_collection.find_one({"_id": ObjectId(id)})
    if student:
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True
