



from agentic_profile_matching.configs.constants import Constants
from agentic_profile_matching.core.ports.console_in import ConsoleIn
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

class PromptToolKitConsoleIn(ConsoleIn):

    def read_line(self, message: str) -> str:
        user_input = prompt(
            message,
            history=FileHistory(Constants.LOGS_PATH),
            auto_suggest=AutoSuggestFromHistory()
        )

        return user_input