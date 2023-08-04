from pydantic import BaseModel


class ImageSchemaCreate(BaseModel):
    is_approved: bool
    root_path: str
    filename: str
    name: str
    thumbnail_path: str

    class Config:
        orm_mode = True