from pydantic import BaseModel


# Модели для ответа в формате JSON

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
    model_config = {"from_attributes": True} # Нужно для SQLAlchemy 2.0

class SubscribeResponse(BaseModel):
    user_id: int
    currency_id: int
    model_config = {"from_attributes": True} # Нужно для SQLAlchemy 2.0

class DeleteResponse(BaseModel):
    status: str
    message: str
    model_config = {"from_attributes": True}  # Нужно для SQLAlchemy 2.0

class SubscriptionDeleteResponse(BaseModel):
    user_id: int
    currency_id: int
    model_config = {"from_attributes": True} # Нужно для SQLAlchemy 2.0