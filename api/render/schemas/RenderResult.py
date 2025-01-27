from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from enum import IntEnum

class RenderStatus(IntEnum):
    OK = 0
    RENDER_ERROR = 1
    UNKNOWN_ERROR = 2

class RenderResult(BaseModel):
    status: RenderStatus
    latex_error: str = Field(default="")
    output_path: Optional[Path] = Field(default=None)
