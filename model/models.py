from pydantic import BaseModel, Field
from typing import List, Union

class Metadata(BaseModel):
    Summary: List[str]
    Title: str
    Author: list[str]
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    language: str
    PageCount: Union [int, str]  # can be 'unknown' if not available
    SentimentTone: str