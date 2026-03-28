




from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    QUIT = "quit"
    EXIT = "exit"
    INGESTION_MAX_WORKERS = 4
    LOGGER_NAME = "apm-logger"
    LOGS_PATH = "logs/prompt.log"
    OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
    RESUMES_DIR_PATH = "src/agentic_profile_matching/resumes"