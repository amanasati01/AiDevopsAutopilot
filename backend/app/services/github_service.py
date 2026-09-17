from app.integrations.github.github_client import GithubClient
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.project_service import get_project_by_projectid
from fastapi import HTTPException,status
import base64
from app.schemas.github import GithubCommitFileContentResponse
async def extract_github_repo(repo_url:str)->tuple[str,str]:
    repo_url = repo_url.rstrip("/")
    parts = repo_url.split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner,repo
async def get_project_repository_data(url:str):
    owner, repo =await extract_github_repo(url)
    github_client  = GithubClient()
    repository_data = await github_client.get_repository(owner,repo)
    return repository_data
async def get_project_github_repository(team_id :UUID, project_id:UUID, db:AsyncSession):
    project =await get_project_by_projectid(project_id,team_id,db)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    repository_data = await get_project_repository_data(project.repo_url)
    return repository_data
async def get_project_github_repository_commits(team_id :UUID, project_id:UUID, db:AsyncSession):
    project =await get_project_by_projectid(project_id,team_id,db)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    github_client = GithubClient()
    owner,repo =await extract_github_repo(project.repo_url)
    commits_data =await github_client.get_commits(owner,repo)
    return commits_data  
async def get_project_github_repository_commit(team_id :UUID,sha:UUID, project_id:UUID, db:AsyncSession):
    project = await get_project_by_projectid(project_id,team_id,db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    github_client = GithubClient()
    owner,repo =await extract_github_repo(project.repo_url)
    commit_data = await github_client.get_commit(owner,repo,sha)
    return commit_data
async def get_project_github_repository_commit_file_content(team_id :UUID,sha:UUID,path:str, project_id:UUID, db:AsyncSession)->GithubCommitFileContentResponse:
    project = await get_project_by_projectid(project_id,team_id,db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    github_client = GithubClient()
    owner,repo =await extract_github_repo(project.repo_url)
    github_data =await github_client.get_file_content(owner,repo,sha,path)
    content = base64.b64decode(
        github_data["content"]
    ).decode("utf-8") 
    return GithubCommitFileContentResponse(
        filename=github_data["name"],
        path=github_data["path"],
        sha=github_data["sha"],
        size=github_data["size"],
        content=content,
        encoding=github_data["encoding"],
    )
async def get_project_github_repository_branches(
    team_id:UUID,
    project_id:UUID,
    db:AsyncSession
):
    project = await get_project_by_projectid(
        project_id,
        team_id,
        db
    )
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    github_client =  GithubClient()
    owner,repo = await extract_github_repo(project.repo_url)
    branches_data = await github_client.get_branches(owner,repo)
    return branches_data
async def get_project_github_repository_branch(
    team_id:UUID,
    project_id:UUID,
    branch:str,
    db:AsyncSession
):
    project = await get_project_by_projectid(project_id,team_id,db)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")
    owner,repo =await extract_github_repo(project.repo_url)
    github_client = GithubClient()
    branch_data = await github_client.get_branch(owner,repo,branch)
    return branch_data
async def get_project_github_repository_languages(
    team_id:UUID,
    project_id:UUID,
    db:AsyncSession
):
    project = await get_project_by_projectid(project_id,team_id,db)
    owner,repo =await extract_github_repo(project.repo_url)
    github_client = GithubClient()
    languages = await github_client.get_langugages(owner,repo)
    return languages
async def get_project_github_repository_contributors(
    team_id:UUID,
    project_id:UUID,
    db:AsyncSession
):
    project =await get_project_by_projectid(project_id,team_id,db)
    owner,repo = await extract_github_repo(project.repo_url)
    github_client = GithubClient()
    contributors_data =await github_client.get_contributors(owner,repo)
    return contributors_data
async def get_project_github_repository_pull_requests(
    team_id:UUID,
    project_id:UUID,
    db:AsyncSession
):
    project =await get_project_by_projectid(project_id,team_id,db)
    owner,repo = await extract_github_repo(project.repo_url)
    github_client = GithubClient()
    pull_requests_data =await github_client.get_pull_requests(owner,repo)
    return pull_requests_data
async def get_project_github_repository_pull_request(
    team_id:UUID,
    project_id:UUID,
    pull_number:int,
    db:AsyncSession
):
    project =await get_project_by_projectid(project_id,team_id,db)
    owner,repo = await extract_github_repo(project.repo_url)
    github_client = GithubClient()
    pull_request_data =await github_client.get_pull_request(owner,repo,pull_number)
    return pull_request_data
async def get_project_github_repository_pull_request_files(
    team_id:UUID,
    project_id:UUID,
    pull_number:int,
    db:AsyncSession
):
    project =await get_project_by_projectid(project_id,team_id,db)
    owner,repo = await extract_github_repo(project.repo_url)
    github_client = GithubClient()
    pull_request_files =await github_client.get_pull_request_files(owner,repo,pull_number)
    return pull_request_files