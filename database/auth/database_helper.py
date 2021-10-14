def user_helper(user) -> dict:
    return {
        "id": str(user['_id']),
        "fullname": user['fullname'],
        "email": user['email'],
    }


def admin_helper(admin) -> dict:
    return user_helper(user=admin)
