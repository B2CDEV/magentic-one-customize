import re
from typing import Awaitable, Callable, List, Literal, Tuple, Union

from autogen_core import CancellationToken, default_subscription
from autogen_core.code_executor import CodeBlock, CodeExecutor
from autogen_core.models import (
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
)

from ..messages import UserContent
from ..utils import message_content_to_str
from .base_worker import BaseWorker


@default_subscription
class Coder(BaseWorker):
    """An agent that can write code or text to solve tasks without additional tools."""

    DEFAULT_DESCRIPTION = "A helpful and general-purpose AI assistant that has strong language skills, Python skills, and Linux command line skills."

    DEFAULT_SYSTEM_MESSAGES = [
        SystemMessage(
            content="""You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply "TERMINATE" in the end when everything is done."""
        )
    ]

    def __init__(
        self,
        model_client: ChatCompletionClient,
        description: str = DEFAULT_DESCRIPTION,
        system_messages: List[SystemMessage] = DEFAULT_SYSTEM_MESSAGES,
        request_terminate: bool = False,
    ) -> None:
        super().__init__(description)
        self._model_client = model_client
        self._system_messages = system_messages
        self._request_terminate = request_terminate

    async def _generate_reply(self, cancellation_token: CancellationToken) -> Tuple[bool, UserContent]:
        """Respond to a reply request."""

        # Make an inference to the model.
        response = await self._model_client.create(
            self._system_messages + self._chat_history, cancellation_token=cancellation_token
        )
        assert isinstance(response.content, str)
        if self._request_terminate:
            return "TERMINATE" in response.content, response.content
        else:
            return False, response.content


# True if the user confirms the code, False otherwise
ConfirmCode = Callable[[CodeBlock], Awaitable[bool]]


@default_subscription
class Reservation(BaseWorker):
    """An agent that can assist with creating and managing reservations using AI capabilities."""

    DEFAULT_DESCRIPTION = "A specialized AI assistant designed to obtain reservation-related information from user."

    DEFAULT_SYSTEM_MESSAGES = [
        SystemMessage(
            content="""You are a specialized AI assistant focused on organizing booking-related information of user. Collect all necessary information for the booking, that is:
   - Date
   - Time
   - Number of people
   - Name"""


    )
    ]
    def __init__(
        self,
        model_client: ChatCompletionClient,
        description: str = DEFAULT_DESCRIPTION,
        system_messages: List[SystemMessage] = DEFAULT_SYSTEM_MESSAGES,
        request_terminate: bool = False,
    ) -> None:
        super().__init__(description)
        self._model_client = model_client
        self._system_messages = system_messages
        self._request_terminate = request_terminate

    async def _generate_reply(self, cancellation_token: CancellationToken) -> Tuple[bool, UserContent]:
        """Respond to a reply request."""

        # Make an inference to the model.
        response = await self._model_client.create(
            self._system_messages + self._chat_history, cancellation_token=cancellation_token
        )
        assert isinstance(response.content, str)
        if self._request_terminate:
            return "TERMINATE" in response.content, response.content
        else:
            return False, response.content


# True if the user confirms the reservation, False otherwise
ConfirmReservation = Callable[[CodeBlock], Awaitable[bool]]


@default_subscription
class Basic(BaseWorker):
    """An AI assistant that provides FAQ support for store-related information."""

    DEFAULT_DESCRIPTION = "A helpful AI assistant specialized in answering FAQs about store information, such as location, hours, services, and policies."

    DEFAULT_SYSTEM_MESSAGES = [
        SystemMessage(
            content="""You are a helpful AI assistant designed to provide FAQ support for store-related inquiries.
Your primary focus is to assist users by answering common questions about the store, such as:
    1. Location: Provide clear and concise details about the store's address and directions.
    2. Operating Hours: Share the store's opening and closing hours, including special holiday schedules if available.
    3. Services: Describe the store's services, including any unique offerings or promotions.
    4. Policies: Clarify store policies on returns, exchanges, or customer support.
    5. Contact Information: Provide phone numbers, email addresses, or other relevant contact methods.
Guidelines:
    - Ensure your responses are accurate, concise, and user-friendly.
    - Provide additional context or clarification when needed to ensure users fully understand the information.
    - If the question involves data you don’t have, state that politely and offer suggestions on how the user can find the information (e.g., visiting the store's website or calling customer service).
    - Avoid using overly technical language unless the user specifically requests it.
    - Always verify the information before providing it to ensure it is up-to-date.
End your response with 'TERMINATE' if the user’s inquiry is fully addressed."""
        )
    ]

    def __init__(
        self,
        model_client: ChatCompletionClient,
        description: str = DEFAULT_DESCRIPTION,
        system_messages: List[SystemMessage] = DEFAULT_SYSTEM_MESSAGES,
        request_terminate: bool = False,
    ) -> None:
        super().__init__(description)
        self._model_client = model_client
        self._system_messages = system_messages
        self._request_terminate = request_terminate

    async def _generate_reply(self, cancellation_token: CancellationToken) -> Tuple[bool, UserContent]:
        """Respond to a reply request."""

        # Make an inference to the model.
        response = await self._model_client.create(
            self._system_messages + self._chat_history, cancellation_token=cancellation_token
        )
        assert isinstance(response.content, str)
        if self._request_terminate:
            return "TERMINATE" in response.content, response.content
        else:
            return False, response.content


# Example of a callable function for confirming store information updates
ConfirmStoreInfo = Callable[[str], Awaitable[bool]]




@default_subscription
class Executor(BaseWorker):
    DEFAULT_DESCRIPTION = "A computer terminal that performs no other action than running Python scripts (provided to it quoted in ```python code blocks), or sh shell scripts (provided to it quoted in ```sh code blocks)"

    def __init__(
        self,
        description: str = DEFAULT_DESCRIPTION,
        check_last_n_message: int = 5,
        *,
        executor: CodeExecutor,
        confirm_execution: ConfirmCode | Literal["ACCEPT_ALL"],
    ) -> None:
        super().__init__(description)
        self._executor = executor
        self._check_last_n_message = check_last_n_message
        self._confirm_execution = confirm_execution

    async def _generate_reply(self, cancellation_token: CancellationToken) -> Tuple[bool, UserContent]:
        """Respond to a reply request."""

        n_messages_checked = 0
        for idx in range(len(self._chat_history)):
            message = self._chat_history[-(idx + 1)]

            if not isinstance(message, UserMessage):
                continue

            # Extract code block from the message.
            code = self._extract_execution_request(message_content_to_str(message.content))

            if code is not None:
                code_lang = code[0]
                code_block = code[1]
                if code_lang == "py":
                    code_lang = "python"
                execution_requests = [CodeBlock(code=code_block, language=code_lang)]
                if self._confirm_execution == "ACCEPT_ALL" or await self._confirm_execution(execution_requests[0]):  # type: ignore
                    result = await self._executor.execute_code_blocks(execution_requests, cancellation_token)

                    if result.output.strip() == "":
                        # Sometimes agents forget to print(). Remind the to print something
                        return (
                            False,
                            f"The script ran but produced no output to console. The Unix exit code was: {result.exit_code}. If you were expecting output, consider revising the script to ensure content is printed to stdout.",
                        )
                    else:
                        return (
                            False,
                            f"The script ran, then exited with Unix exit code: {result.exit_code}\nIts output was:\n{result.output}",
                        )
                else:
                    return (
                        False,
                        "The code block was not confirmed by the user and so was not run.",
                    )
            else:
                n_messages_checked += 1
                if n_messages_checked > self._check_last_n_message:
                    break

        return (
            False,
            "No code block detected in the messages. Please provide a markdown-encoded code block to execute for the original task.",
        )

    def _extract_execution_request(self, markdown_text: str) -> Union[Tuple[str, str], None]:
        pattern = r"```(\w+)?(\n|\w)?(.*?)(\n)?```"
        # Search for the pattern in the markdown text
        match = re.search(pattern, markdown_text, re.DOTALL)
        # Extract the language and code block if a match is found
        if match:
            return ("sh", match.group(3))
        return None
