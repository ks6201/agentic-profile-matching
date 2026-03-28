


from typing import Generic, Protocol, TypeVar

INPUT_TYPE = TypeVar("INPUT_TYPE", contravariant=True)
OUTPUT_TYPE = TypeVar("OUTPUT_TYPE", covariant=True)

class Step(Protocol, Generic[INPUT_TYPE, OUTPUT_TYPE]):

    def execute(self, input: INPUT_TYPE) -> OUTPUT_TYPE:
        ...