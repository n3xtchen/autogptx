"""Git operations for autogpt"""
from git.repo import Repo

from autogpt.commands.command import command
from autogpt.config import Config
from autogpt.url_utils.validators import validate_url

CFG = Config()


@command(
    "clone_repository",
    # "Clone Repository",
    "克隆代码仓库",
    # '"url": "<repository_url>", "clone_path": "<clone_path>"',
    '"url": "<repository_url>", "clone_path": "<clone_path>"',
    CFG.github_username and CFG.github_api_key,
    # "Configure github_username and github_api_key.",
    "配置 github_username 和 github_api_key。",
)
@validate_url
def clone_repository(url: str, clone_path: str) -> str:
    """Clone a GitHub repository locally.

    Args:
        url (str): The URL of the repository to clone.
        clone_path (str): The path to clone the repository to.

    Returns:
        str: The result of the clone operation.
    """
    split_url = url.split("//")
    auth_repo_url = f"//{CFG.github_username}:{CFG.github_api_key}@".join(split_url)
    try:
        Repo.clone_from(url=auth_repo_url, to_path=clone_path)
        # return f"""Cloned {url} to {clone_path}"""
        return f"""克隆 {url} 到 {clone_path}"""
    except Exception as e:
        return f"错误: {str(e)}"
