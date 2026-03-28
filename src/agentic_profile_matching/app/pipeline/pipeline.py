
from typing import Any, Generic, TypeVar

from agentic_profile_matching.app.pipeline.step import Step

INPUT_TYPE = TypeVar("INPUT_TYPE")
OUTPUT_TYPE = TypeVar("OUTPUT_TYPE")
PIPE_OUTPUT_TYPE = TypeVar("PIPE_OUTPUT_TYPE")

START_INPUT_TYPE = TypeVar("START_INPUT_TYPE")
START_OUTPUT_TYPE = TypeVar("START_OUTPUT_TYPE")

class Pipeline(Generic[INPUT_TYPE, OUTPUT_TYPE]):

    def __init__(self, steps: list[Step[INPUT_TYPE, OUTPUT_TYPE]]) -> None:
        super().__init__()
        self.steps: list[Any] = steps

    @staticmethod
    def start(step: Step[START_INPUT_TYPE, START_OUTPUT_TYPE]) -> "Pipeline[START_INPUT_TYPE, START_OUTPUT_TYPE]":
        return Pipeline([step])

    def pipe(self, step: Step[OUTPUT_TYPE, PIPE_OUTPUT_TYPE]) -> "Pipeline[INPUT_TYPE, PIPE_OUTPUT_TYPE]":
        return Pipeline(self.steps + [step])

    def run(self, input: INPUT_TYPE) -> OUTPUT_TYPE:
        output: Any = input

        for step in self.steps:
            output = step.execute(output)

        return output
