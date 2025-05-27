from pydantic import BaseModel


class UserProfile(BaseModel):

    first_name: str = ""
    last_name: str = ""
    user_id: str = ""
    birth_date: str = ""
    city: str = ""
    is_closed: str = ""
    online: str = ""


