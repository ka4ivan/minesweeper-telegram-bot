from pydantic import BaseModel

class CustomSettings(BaseModel):
    width: int
    height: int
    mines: int
