from pydantic import BaseModel, Field
from typing import Optional

class Rating(BaseModel):
    app_id: str
    entity_id: str
    user_id: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None