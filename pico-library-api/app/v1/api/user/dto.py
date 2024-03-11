from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, DateTime, Float, Nested


user_model = Model("User", {"email": String, "public_id": String})


profile_model = Model(
    "Profile",
    {
        "first_name": String,
        "last_name": String,
        "gender": String(attribute="gender_str"),
        "bio": String,
        "location": String,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
        "user": Nested(user_model),
    },
)
