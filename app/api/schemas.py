from pydantic import BaseModel, Field
from typing import List, Dict

class PredictRequest(BaseModel):
    subject: str = Field(..., description="Subject of the support ticket")
    description: str = Field(..., description="Detailed description of the issue")


class Resolution(BaseModel):
    subject: str
    description: str
    resolution: str
    similarity: float


class PredictResponse(BaseModel):
    type: str
    priority: str
    type_exp: Dict[str, float] = Field(..., description="Local feature contributions for category prediction")
    prio_exp: Dict[str, float] = Field(..., description="Local feature contributions for priority prediction")
    resolutions: List[Resolution] = Field(..., description="Top 3 recommended historical resolutions")
