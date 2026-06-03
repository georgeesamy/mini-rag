from .LLMEnums import LLMEnums
from .providers import OpenAIProvider, CoHereProvider
from typing import Any

class LLMProviderFactory:
    def __init__(self, config: Any):
        self.config = config        #think of this as configuration import 

    def create_provider(self, provider_name: str):
        if provider_name == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config["OPENAI_API_KEY"],
                api_url=self.config["OPENAI_API_URL"],
                default_input_max_characters=self.config["DEFAULT_INPUT_MAX_CHARACTERS"],
                default_output_max_characters=self.config["DEFAULT_OUTPUT_MAX_CHARACTERS"],
                default_generation_temperature=self.config["DEFAULT_GENERATION_TEMPERATURE"]
            )

        if provider_name == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config["COHERE_API_KEY"],
                default_input_max_characters=self.config["DEFAULT_INPUT_MAX_CHARACTERS"],
                default_output_max_characters=self.config["DEFAULT_OUTPUT_MAX_CHARACTERS"],
                default_generation_temperature=self.config["DEFAULT_GENERATION_TEMPERATURE"]
            )

        return None