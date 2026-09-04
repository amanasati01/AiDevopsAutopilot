import asyncio

from app.integrations.github.github_client import GithubClient


async def main():
    github_client = GithubClient()

    commits = await github_client.get_commits(
        "amanasati01",
        "Aman-Asati",
    )

    print(commits[0])


asyncio.run(main())