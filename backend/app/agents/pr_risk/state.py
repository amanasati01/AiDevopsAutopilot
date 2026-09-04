from typing import TypedDict

class PRRiskState(TypedDict):
    team_id: str
    project_id: str
    pull_number: int
    pr_data: dict
    pr_files: list[dict]
    risk_analysis : dict
