from app.services.github_service import get_project_github_repository,get_project_github_repository_commits,get_project_github_repository_commit, get_project_github_repository_commit_file_content,get_project_github_repository_branches,get_project_github_repository_languages,get_project_github_repository_branch,get_project_github_repository_contributors,get_project_github_repository_pull_requests,get_project_github_repository_pull_request,get_project_github_repository_pull_request_files
from fastapi import APIRouter,Depends
from uuid import UUID
from app.core.dependency import get_current_user
from app.core.authorization import require_team_role
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.github import GithubRepositoryResponse,GithubCommitResponse,GithubCommitDetailResponse,GithubCommitFileResponse,GithubBranchesResponse,GithubCommitFileContentResponse,GithubBranchResponse,GithubContributorResponse,GithubPullRequestListResponse,GithubPullRequestDetailResponse,GithubPullRequestFileResponse
from app.agents.pr_risk.graph import build_pr_risk_graph
from app.agents.pr_risk.context import PRRiskContext
router = APIRouter(
    prefix="/teams/{team_id}/projects/{project_id}/github",
    tags=["GitHub"],
)
@router.get("/repository")
async def get_github_repository(
    team_id:UUID,
    project_id:UUID,
    db:AsyncSession=Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER","ADMIN","MEMBER"))
):
    data = await get_project_github_repository(team_id,project_id,db)
    repository_data = GithubRepositoryResponse(
        id=data["id"],
        name=data["name"],
        full_name=data["full_name"],
        description=data["description"],
        private=data["private"],
        html_url=data["html_url"],
        default_branch=data["default_branch"],
        language=data["language"],
        stargazers_count=data["stargazers_count"],
        forks_count=data["forks_count"],
        open_issues_count=data["open_issues_count"]
        )
    return repository_data
@router.get("/repository/commits",
    response_model=list[GithubCommitResponse]
)
async def get_commits(
    team_id: UUID,
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))
):
    data = await get_project_github_repository_commits(
        team_id,
        project_id,
        db
    )

    commits = [
        GithubCommitResponse(
            sha=commit["sha"],
            message=commit["commit"]["message"],
            author_name=commit["commit"]["author"]["name"],
            author_email=commit["commit"]["author"]["email"],
            committed_at=commit["commit"]["author"]["date"],
            html_url=commit["html_url"]
        )
        for commit in data
    ]

    return commits
@router.get("/repository/commit/{sha}",response_model=GithubCommitDetailResponse)
async def get_commit(
    team_id: UUID,
    project_id: UUID,
    sha:str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))
):
    commit =await get_project_github_repository_commit(team_id,sha,project_id,db)
    print(commit)
    return GithubCommitDetailResponse(   
        sha=commit["sha"],
        message=commit["commit"]["message"],
        author_name=commit["commit"]["author"]["name"],
        author_email=commit["commit"]["author"]["email"],
        committed_at=commit["commit"]["author"]["date"],
        html_url=commit["html_url"],
        files_changed=len(commit["files"]),
        additions=commit["stats"]["additions"],
        deletions=commit["stats"]["deletions"]
)
@router.get("/repository/commit/{sha}/files",response_model=list[GithubCommitFileResponse])
async def get_commit_files(
    team_id: UUID,
    project_id: UUID,
    sha:str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))
):
    commit = await get_project_github_repository_commit(
        team_id,
        sha,
        project_id,
        db
    )

    files = [
        GithubCommitFileResponse(
            filename=file["filename"],
            status=file["status"],
            additions=file["additions"],
            deletions=file["deletions"],
            changes=file["changes"],
            patch=file.get("patch")
        )
        for file in commit["files"]
    ]
    return files
@router.get("/repository/commit/{sha}/file",response_model=GithubCommitFileContentResponse)
async def get_file_content(
    team_id: UUID,
    path:str,
    project_id: UUID,
    sha:str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))
):
    return await get_project_github_repository_commit_file_content(team_id,sha,path,project_id,db)
@router.get("/repository/branches",response_model=list[GithubBranchesResponse])
async def get_repo_branches(
    team_id: UUID,
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))
):
    data = await get_project_github_repository_branches(team_id,project_id,db)
    print(data)
    branches= [
        GithubBranchesResponse(
            name=branch["name"],
            sha=branch["commit"]["sha"],
            url=branch["commit"]["url"],
            protected=branch["protected"]
        )
        for branch in data
    ]
    return branches
@router.get("/repository/branch/{branch}")
async def get_brach_details(
    team_id: UUID,
    project_id: UUID,
    branch:str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))
):
    branch =await get_project_github_repository_branch(team_id,project_id,branch,db)
    # print(branch)
    return GithubBranchResponse(
        name=branch["name"],
        sha=branch["commit"]["sha"],
        url=branch["commit"]["url"],
        protected=branch["protected"]
    )
@router.get("/repository/languages")
async def get_languages(
    team_id: UUID,
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER"))  
):
    languages = await get_project_github_repository_languages(team_id,project_id,db)
    return languages
@router.get("/repository/contributors",response_model=list[GithubContributorResponse])
async def get_contributors(
    team_id: UUID,
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER")) 
):
    contributors_data = await get_project_github_repository_contributors(team_id,project_id,db)
    contributors = [
    GithubContributorResponse(
        login=contributor["login"],
        id=contributor["id"],
        avatar_url=contributor["avatar_url"],
        html_url=contributor["html_url"],
        contributions=contributor["contributions"],
    )
    for contributor in contributors_data
]
    return contributors
@router.get("/repository/pulls",response_model=list[GithubPullRequestListResponse])
async def get_pull_requests(
    team_id: UUID,
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER")) 
):
    pull_requests_data = await get_project_github_repository_pull_requests(team_id,project_id,db)
    pull_requests = [
    GithubPullRequestListResponse(
        number=pull["number"],
        title=pull["title"],
        state=pull["state"],
        user_login=pull["user"]["login"],
        user_avatar_url=pull["user"]["avatar_url"],
        html_url=pull["html_url"],
        created_at=pull["created_at"],
        updated_at=pull["updated_at"],
        closed_at=pull["closed_at"],
        merged_at=pull["merged_at"],
        draft=pull["draft"],
    )
    for pull in pull_requests_data
]

    return pull_requests
@router.get("/repository/pull/{pull_number}",response_model=GithubPullRequestDetailResponse)
async def get_pull_requests(
    team_id: UUID,
    project_id: UUID,
    pull_number:int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER")) 
):
    data = await get_project_github_repository_pull_request(team_id,project_id,pull_number,db)
    return GithubPullRequestDetailResponse(
    number=data["number"],
    title=data["title"],
    state=data["state"],
    user_login=data["user"]["login"],
    user_avatar_url=data["user"]["avatar_url"],
    body=data["body"],
    html_url=data["html_url"],
    created_at=data["created_at"],
    updated_at=data["updated_at"],
    closed_at=data["closed_at"],
    merged_at=data["merged_at"],
    draft=data["draft"],
    mergeable=data["mergeable"],
    additions=data["additions"],
    deletions=data["deletions"],
    changed_files=data["changed_files"],
)
@router.get("/repository/pull/{pull_number}/files",response_model=list[GithubPullRequestFileResponse])
async def get_pull_requests(
    team_id: UUID,
    project_id: UUID,
    pull_number:int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    membership=Depends(require_team_role("OWNER", "ADMIN", "MEMBER")) 
):
    data = await get_project_github_repository_pull_request_files(team_id,project_id,pull_number,db)
    files = [
        GithubPullRequestFileResponse(
            sha=file["sha"],
            filename=file["filename"],
            status=file["status"],
            additions=file["additions"],
            deletions=file["deletions"],
            changes=file["changes"],
            patch=file.get("patch"),
        )
        for file in data
    ]

    return files
@router.get("/repository/pull/{pull_number}/risk-analysis")
async def analysis_pull_request(
    team_id:UUID,
    project_id:UUID,
    pull_number:int,
    db:AsyncSession = Depends(get_db),
    membership = Depends(require_team_role("OWNER","ADMIN","MEMBER")),
    current_user = Depends(get_current_user)
):
    graph = build_pr_risk_graph() 
    initial_state = {
        "team_id" : str(team_id),
        "project_id" : str(project_id),
        "pull_number" : pull_number,
        "pr_data" : {},
        "pr_files" : [] 
    }
    context = PRRiskContext(db)
    result =  await graph.ainvoke(
        initial_state,
        context=context
    )
    return result 