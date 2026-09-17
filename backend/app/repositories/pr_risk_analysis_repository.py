from app.models.pr_risk_analysis import PRRiskAnalysis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
class pr_risk_analysis_repository:
    def __init__(self,db:AsyncSession):
        self.db = db
        
    async def get_by_pull_number(
        self,
        team_id,
        project_id,
        pull_number,
    ):
        analysis =await self.db.execute(
            select(PRRiskAnalysis).where(
                PRRiskAnalysis.pull_number == pull_number,
                PRRiskAnalysis.project_id == project_id,
                PRRiskAnalysis.team_id == team_id
            ).order_by(PRRiskAnalysis.created_at.asc())
        )
        print("analysis ", analysis)
        return analysis.scalars().all()
    
        