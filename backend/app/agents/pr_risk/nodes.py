from .state import PRRiskState
from langgraph.runtime import Runtime
from .context import PRRiskContext

from app.services.github_service import (
    get_project_github_repository_pull_request,
    get_project_github_repository_pull_request_files,
)


async def fetch_pr(
    state: PRRiskState,
    runtime: Runtime[PRRiskContext],
) -> dict:

    pr_data = await get_project_github_repository_pull_request(
        state["team_id"],
        state["project_id"],
        state["pull_number"],
        runtime.context.db,
    )

    return {
        "pr_data": pr_data
    }


async def fetch_pr_files(
    state: PRRiskState,
    runtime: Runtime[PRRiskContext],
) -> dict:

    pr_file_data = await get_project_github_repository_pull_request_files(
        state["team_id"],
        state["project_id"],
        state["pull_number"],
        runtime.context.db,
    )

    return {
        "pr_files": pr_file_data
    }
# async def analyse_pr(
#     state : PRRiskState,
#     runtime : Runtime[PRRiskContext]
# ):
    