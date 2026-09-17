from pydantic import BaseModel,Field
from typing import Literal

class RiskItem(BaseModel):
    title: str
    description: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]


class Recommendation(BaseModel):
    title: str
    description: str


class PRRiskAnalysisOutput(BaseModel):
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    risk_score: int = Field(ge=0, le=10)
    summary: str
    security_concerns: list[RiskItem]
    breaking_changes: list[RiskItem]
    risk: list[RiskItem]
    recommendation: list[Recommendation]
class PRRiskAnalysisResponse(BaseModel):
    pull_request: dict
    analysis:list[PRRiskAnalysisOutput]