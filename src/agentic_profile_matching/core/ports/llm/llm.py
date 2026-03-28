# from abc import ABC, abstractmethod


# class LLM(ABC):

#     def __init__(self, tools_registry: ToolsRegistry):
#         self._tools_registry = tools_registry

#     @abstractmethod
#     def generate(self, llm_input: LLMInput) -> Result[LLMResponse, str]:
#         ...

#     @abstractmethod
#     def close(self):
#         ...