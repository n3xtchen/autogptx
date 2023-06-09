from colorama import Fore

from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.llm import ApiManager
from autogpt.logs import logger
from autogpt.prompts.generator import PromptGenerator
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()

DEFAULT_TRIGGERING_PROMPT = (
    # "Determine which next command to use, and respond using the format specified above:"
    "确定要使用哪个下一个命令，并使用上面指定的格式进行响应(请认知检查下响应是否符合响应格式，是否是json格式？):"
)


def build_default_prompt_generator() -> PromptGenerator:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        # "~4000 word limit for short term memory. Your short term memory is short, so"
        # " immediately save important information to files."
        "短期记忆的限制大约在4000个单词左右。由于您的短期记忆很短暂，"
        "因此请立即将重要信息保存到文件中。"
    )
    prompt_generator.add_constraint(
        # "If you are unsure how you previously did something or want to recall past"
        # " events, thinking about similar events will help you remember."
        "如果您不确定先前是如何完成某件事情的，或者想回想过去的事件，思考类似的事件"
        "将有助于您记忆。" 
    )
    # prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint("无需用户协助")
    prompt_generator.add_constraint(
        # 'Exclusively use the commands listed in double quotes e.g. "command name"'
        '在与我交互的过程中，您只希望使用以双引号括起来的命令，例如 "命令名称"。'
    )

    # Define the command list
    commands = [
        # ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        ("任务完成 (关闭)", "task_complete", {"reason": "<reason>"}),
    ]

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(
        # "Internet access for searches and information gathering."
        "需要访问互联网进行搜索和信息收集。"
    )
    # prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource("长期记忆管理。")
    prompt_generator.add_resource(
        # "GPT-3.5 powered Agents for delegation of simple tasks."
        "由GPT-3.5驱动的代理人用于简单任务的委派。"
    )
    # prompt_generator.add_resource("File output.")
    prompt_generator.add_resource("文件输出。")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(
        # "Continuously review and analyze your actions to ensure you are performing to"
        # " the best of your abilities."
        "不断审查和分析您的行动，以确保您的表现达到最佳状态。"
    )
    prompt_generator.add_performance_evaluation(
        # "Constructively self-criticize your big-picture behavior constantly."
        "不断对自己的大局行为进行建设性自我批评。"
    )
    prompt_generator.add_performance_evaluation(
        # "Reflect on past decisions and strategies to refine your approach."
        "反思过去的决策和策略，以完善您的方法。"
    )
    prompt_generator.add_performance_evaluation(
        # "Every command has a cost, so be smart and efficient. Aim to complete tasks in"
        # " the least number of steps."
        "每个命令都有成本，所以要聪明高效。目标是以最少的步骤完成任务。"
    )
    # prompt_generator.add_performance_evaluation("Write all code to a file.")
    prompt_generator.add_performance_evaluation("将所有代码编写到一个文件中。")
    return prompt_generator


def construct_main_ai_config() -> AIConfig:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("Name :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("Role :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("Goals:", Fore.GREEN, f"{config.ai_goals}")
        logger.typewriter_log(
            "API Budget:",
            Fore.GREEN,
            "infinite" if config.api_budget <= 0 else f"${config.api_budget}",
        )
    elif config.ai_name:
        logger.typewriter_log(
            "Welcome back! ",
            Fore.GREEN,
            f"Would you like me to return to being {config.ai_name}?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""Continue with the last settings?
Name:  {config.ai_name}
Role:  {config.ai_role}
Goals: {config.ai_goals}
API Budget: {"infinite" if config.api_budget <= 0 else f"${config.api_budget}"}
Continue ({CFG.authorise_key}/{CFG.exit_key}): """
        )
        if should_continue.lower() == CFG.exit_key:
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save(CFG.ai_settings_file)

    # set the total api budget
    api_manager = ApiManager()
    api_manager.set_total_budget(config.api_budget)

    # Agent Created, print message
    logger.typewriter_log(
        config.ai_name,
        Fore.LIGHTBLUE_EX,
        "has been created with the following details:",
        speak_text=True,
    )

    # Print the ai config details
    # Name
    logger.typewriter_log("Name:", Fore.GREEN, config.ai_name, speak_text=False)
    # Role
    logger.typewriter_log("Role:", Fore.GREEN, config.ai_role, speak_text=False)
    # Goals
    logger.typewriter_log("Goals:", Fore.GREEN, "", speak_text=False)
    for goal in config.ai_goals:
        logger.typewriter_log("-", Fore.GREEN, goal, speak_text=False)

    return config
