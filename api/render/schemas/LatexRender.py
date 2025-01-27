from pydantic import BaseModel

class LatexRenderRequest(BaseModel):
    document: str
