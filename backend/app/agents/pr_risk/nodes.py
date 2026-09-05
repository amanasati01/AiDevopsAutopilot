from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .state import PRRiskState
from langgraph.runtime import Runtime
from .context import PRRiskContext
from .schema import PRRiskAnalysis
from app.services.github_service import (
    get_project_github_repository_pull_request,
    get_project_github_repository_pull_request_files,
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
structured_llm = llm.with_structured_output(PRRiskAnalysis)
async def analyse_pr(state:PRRiskState)->dict:
    pr_data = state["pr_data"]
    pr_files = state["pr_files"]
    prompt = f"""
You are a senior software engineer performing a production-grade
GitHub Pull Request risk assessment.

Analyze ONLY the information provided below.
Do not invent files, bugs, vulnerabilities, or behavior that is not
supported by the PR data or changed files.

====================
PULL REQUEST
====================

{pr_data}

====================
CHANGED FILES
====================

{pr_files}

====================
ANALYSIS REQUIREMENTS
====================

1. SUMMARY
Explain what this PR actually changes.

2. RISK ANALYSIS
Identify concrete risks introduced by the changes.

For every risk:
- Give a short title.
- Explain the problem clearly.
- Identify the relevant file when possible.
- Assign severity: LOW, MEDIUM, or HIGH.

Do NOT report a risk merely because a change "could potentially"
cause something. There must be reasonable evidence in the provided
changes.

3. SECURITY
Look specifically for:
- Authentication/authorization changes
- Secrets or credentials
- Injection vulnerabilities
- Unsafe user input handling
- Permission changes
- Sensitive data exposure
- Dependency/security configuration changes

If there is no security concern, do not invent one.

4. BREAKING CHANGES
Check for:
- API contract changes
- Removed/renamed functionality
- Database/schema changes
- Changed function signatures
- Configuration changes
- Changes that could break existing consumers

If none exist, state that there are no apparent breaking changes.

5. RISK SCORE

Calculate a score from 0 to 10:

0-2  = LOW
3-5  = MEDIUM
6-10 = HIGH

The risk_score and risk_level MUST be consistent.

6. RECOMMENDATIONS
Provide concrete actions the developer should take before merging.

Do not give generic advice such as "review the code carefully"
unless it is directly relevant to a detected risk.

====================
OUTPUT RULES
====================

Return only the structured analysis matching the provided schema.

Keep the analysis concise but technically specific.
"""
    response = await structured_llm.ainvoke([HumanMessage(content=prompt)])
    return{
        "risk_analysis" : response.model_dump()
    }

    
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
    