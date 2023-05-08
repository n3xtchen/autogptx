"""A module that contains a function to generate test cases for the submitted code."""
from __future__ import annotations

import json

from autogpt.commands.command import command
from autogpt.llm import call_ai_function


@command(
    "write_tests",
    # "Write Tests",
    "编写测试",
    # '"code": "<full_code_string>", "focus": "<list_of_focus_areas>"',
    '"code": "<完整的代码字符串>", "focus": "<关注的领域列表>"',
)
def write_tests(code: str, focus: list[str]) -> str:
    """
    A function that takes in code and focus topics and returns a response from create
      chat completion api call.

    Parameters:
        focus (list): A list of suggestions around what needs to be improved.
        code (str): Code for test cases to be generated against.
    Returns:
        A result string from create chat completion. Test cases for the submitted code
          in response.
    """

    function_string = (
        "def create_test_cases(code: str, focus: Optional[str] = None) -> str:"
    )
    args = [code, json.dumps(focus)]
    description_string = (
        # "Generates test cases for the existing code, focusing on"
        # " specific areas if required."
        "生成现有代码的测试用例，如果需要则着重于特定领域。"
    )

    return call_ai_function(function_string, args, description_string)
