from pydantic import BaseModel
from datetime import datetime
class GithubRepositoryResponse(BaseModel):
    id: int
    name: str
    full_name: str
    description: str | None
    private: bool
    html_url: str
    default_branch: str
    language: str | None
    stargazers_count: int
    forks_count: int
    open_issues_count: int
class GithubCommitResponse(BaseModel):
    sha: str
    message: str
    author_name: str
    author_email: str
    committed_at: datetime
    html_url: str
class GithubCommitDetailResponse(BaseModel):
    sha: str
    message: str
    author_name: str
    author_email: str
    committed_at: str
    html_url: str
    files_changed: int
    additions: int
    deletions: int
class GithubCommitFileResponse(BaseModel):
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: str | None = None
class GithubCommitFileContentResponse(BaseModel):
    filename: str
    path: str
    sha: str
    size: int
    content: str
    encoding: str
class GithubBranchesResponse(BaseModel):
    name: str
    sha: str
    url:str
    protected: bool
class GithubBranchResponse(BaseModel):
    name: str
    sha: str
    url: str
    protected: bool
class GithubContributorResponse(BaseModel):
    login: str
    id: int
    avatar_url: str
    html_url: str
    contributions: int
class GithubPullRequestListResponse(BaseModel):
    number: int
    title: str
    state: str
    user_login: str
    user_avatar_url: str
    html_url: str
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None
    merged_at: datetime | None
    draft: bool
class GithubPullRequestDetailResponse(BaseModel):
    number: int
    title: str
    state: str

    user_login: str
    user_avatar_url: str

    body: str | None
    html_url: str

    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None
    merged_at: datetime | None

    draft: bool
    mergeable: bool | None

    additions: int
    deletions: int
    changed_files: int
class GithubPullRequestFileResponse(BaseModel):
    sha: str
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    patch: str | None