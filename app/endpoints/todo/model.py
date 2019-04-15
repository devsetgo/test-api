from typing import List, Optional, Union
from pydantic import BaseModel, Schema, Json, UUID1
import uuid
from datetime import datetime,timedelta
import json

def id_create() -> str:
    result = uuid.uuid1()
    # print(result)
    return result

def current_time():
    currentTime = datetime.now()
    return currentTime

def daysPlus30():
    result = current_time() + timedelta(days=30)
    return result

class ToDoBase(BaseModel):
    id: Optional[str]
    title: str
    description: Optional[str]
    isComplete: Optional[bool] = False
    dateDue: Optional[str] = daysPlus30()
    dateCreate: Optional[str] = str(current_time())
    dateUpdate: datetime = str(current_time())
    dateComplete: Optional[str]
    userId: str

        

# Properties to receive via API on creation
# Additional properties to return via API
class ToDoInDB(ToDoBase):
    id: str

# Create a ToDo
class TodoCreate(BaseModel):
    title: str
    description: str = None
    dateDue: str = None
    userId: str =None

    
    #date_information: ToDoDateInformation = Schema(None)

# Create a ToDo
class TodoGetId(ToDoBase):
    id: str
    
# Update a ToDo
class TodoUpdate(ToDoBase):
    id: str
    title: str
    description: str
    isComplete: Optional[bool] = False
    dateDue: Optional[str]

# complete a ToDo
class TodoUpdateComplete(ToDoBase):
    id: str
    isComplete: bool = True

# Delete a ToDo
class TodoDelete(ToDoBase):
    id: str


