from pydantic import BaseModel,RootModel, Field
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

class ChangeFormat(BaseModel):
    Page: str
    Changes: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass