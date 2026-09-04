import httpx


class GithubClient:
    BASE_URL = "https://api.github.com"

    async def get_repository(
        self,
        owner: str,
        repo: str,
    ):
        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}"
            )

            response.raise_for_status()

            return response.json()
    async def get_commits(
        self,
        owner: str,
        repo: str,
    ):
        async with httpx.AsyncClient() as client:
            reponse = await client.get(f"{self.BASE_URL}/repos/{owner}/{repo}/commits")
            reponse.raise_for_status()
            return reponse.json()
    async def get_commit(
        self,
        owner: str,
        repo: str,
        sha: str
    ):
        
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/commits/{sha}"
            response = await client.get(url)
            response.raise_for_status
            return response.json()
    async def get_file_content(
        self,
        owner:str,
        repo:str,
        sha:str,
        path:str
    ):
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}?ref={sha}"
            response = await client.get(
                url,
                params={"ref":sha}
            )
            response.raise_for_status()
            return response.json()
    async def get_branches(
        self,
        owner:str,
        repo:str
    ):
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/branches"
            response =await client.get(url)
            response.raise_for_status()
            return response.json()
    async def get_branch(
        self,
        owner:str,
        repo:str,
        branch:str
    ):
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/branches/{branch}"
            repsonse =await client.get(url)
            repsonse.raise_for_status()
            return repsonse.json()
    async def get_langugages(
        self,
        owner:str,
        repo:str
    ):
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/languages"
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    async def get_contributors(
        self,
        owner,
        repo
    ):
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/contributors"
            contributors_data = await client.get(url)
            contributors_data.raise_for_status()
            return contributors_data.json()
    async def get_pull_requests(
        self,
        owner,
        repo
    ):
        async with httpx.AsyncClient() as client:
                    url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"
                    pull_requests_data = await client.get(url)
                    pull_requests_data.raise_for_status()
                    print(pull_requests_data.json())
                    return pull_requests_data.json()
    async def get_pull_request(
        self,
        owner,
        repo,
        pull_number
    ):
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}"
            pull_request_data = await client.get(url)
            pull_request_data.raise_for_status()
            return pull_request_data.json()
    async def get_pull_request_files(
            self,
            owner,
            repo,
            pull_number
        ):
            async with httpx.AsyncClient() as client:
                url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}/files"
                pull_request_files = await client.get(url)
                pull_request_files.raise_for_status()
                return pull_request_files.json()
            
      
        
    
