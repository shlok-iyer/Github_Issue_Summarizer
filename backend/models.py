from pydantic import BaseModel, HttpUrl, Field

class AnalyzeRequest(BaseModel):
    repo_url: HttpUrl
    issue_number: int = Field(ge=1)

class AnalysisJSON(BaseModel):
    summary: str
    type: str  # one of: bug, feature_request, documentation, question, other
    priority_score: str  # "1".."5" with brief justification
    suggested_labels: list[str]
    potential_impact: str

class AnalyzeResponse(BaseModel):
    repo: str
    issue_number: int
    issue_url: str
    analysis: AnalysisJSON
