 # Request/response shapes
 
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str
    routed_to: str
    complexity: str