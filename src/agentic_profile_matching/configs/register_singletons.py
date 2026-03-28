

from langchain_openai import ChatOpenAI


from agentic_profile_matching.adapters.console._in.prompt_toolkit_console_in import PromptToolKitConsoleIn
from agentic_profile_matching.adapters.console.out.markdown_console_out import MarkdownConsoleOut
from agentic_profile_matching.adapters.db.db import Database
from agentic_profile_matching.adapters.file_io.file_io_factory import FileIOFactory
from agentic_profile_matching.app.utils.container import Container
from agentic_profile_matching.configs.envs import Env
from agentic_profile_matching.core.ports.console_in import ConsoleIn
from agentic_profile_matching.core.ports.console_out import ConsoleOut


def register_singletons():
    Container.singleton(
        Env,
        lambda: Env()
    )

    Container.singleton(
        Database,
        lambda: Database()
    )

    Container.singleton(
        FileIOFactory,
        lambda: FileIOFactory
    )

    Container.singleton(
        ConsoleIn,
        lambda: PromptToolKitConsoleIn()
    )

    Container.singleton(
        ConsoleOut,
        lambda: MarkdownConsoleOut()
    )

    Container.singleton(
        ChatOpenAI,
        lambda: ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
    )