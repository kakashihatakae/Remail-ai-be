from pydantic import BaseModel
from typing import Union


class JobDescription(BaseModel):
    userId: str
    title: str
    location: Union[str, None] = None
    onsite_remote: Union[str, None] = None
    duration: Union[str, None] = None
    contract_type: Union[str, None] = None
    visa: Union[str, None] = None
    experience: Union[str, None] = None
    rate: Union[str, None] = None
    skills: str
