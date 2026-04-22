from pydantic import BaseModel

class VideoCreate(BaseModel):
    title: str
    video_url: str
    content_duration_seconds: int
    advert_duration_seconds: int = 0

class VideoOut(BaseModel):
    id: int
    title: str
    video_url: str
    likes: int
    views: int
    earnings: float
    status: str
