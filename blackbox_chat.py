from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import cloudscraper
from concurrent.futures import ThreadPoolExecutor

class ChatModel(Enum):
    """Available chat models for the BlackBox API."""
    GPT_4O = "gpt-4o"
    GEMINI_PRO = "gemini-pro"
    CLAUDE_SONNET_35 = "claude-sonnet-3.5"
    BLACKBOX_AI_PRO = "blackboxai-pro"
    BLACKBOX_AI = "blackboxai"

class BlackBoxError(Exception):
    """Base exception class for BlackBox API related errors."""
    pass

class ModelNotFoundError(BlackBoxError):
    """Exception raised when an invalid model is specified."""
    pass

class APIRequestError(BlackBoxError):
    """Exception raised when API requests fail."""
    pass

@dataclass
class ChatConfig:
    """Configuration for chat requests."""
    max_tokens: int = 1024
    deep_search_mode: bool = True
    web_search_mode_prompt: bool = True
    timeout: int = 30

class BlackBoxChat:
    """Main class for interacting with BlackBox chat functionality."""
    
    def __init__(self, config: Optional[ChatConfig] = None):
        """
        Initialize BlackBox Chat.
        
        Args:
            config: Optional ChatConfig object. If not provided, default config will be used.
        """
        self.config = config or ChatConfig()
        self.scraper = cloudscraper.create_scraper()
        self.base_url = "https://www.blackbox.ai/api"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.blackbox.ai',
            'priority': 'u=1, i',
            'referer': 'https://www.blackbox.ai/',
            'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    def _send_sources_request(self, query: str) -> Dict[str, Any]:
        """Send request to check sources endpoint."""
        try:
            data = {
                'query': query,
                'messages': [{'content': query, 'role': 'user', 'id': ''}],
                'index': None
            }
            response = self.scraper.post(
                f"{self.base_url}/check",
                headers=self._get_headers(),
                json=data,
                timeout=self.config.timeout
            )
            if response.status_code == 200:
                return {"sources": response.json()}
            raise APIRequestError(f"Sources request failed with status code: {response.status_code}")
        except Exception as e:
            raise APIRequestError(f"Sources request failed: {str(e)}")

    def _send_chat_request(self, query: str, model: ChatModel, prints: bool = True) -> Dict[str, Any]:
        """Send request to chat endpoint."""
        try:
            data = {
                'messages': [
                    {
                        'id': '',
                        'content': f"@{model.value} {query}",
                        'role': 'user',
                    },
                ],
                'id': '',
                'previewToken': None,
                'userId': None,
                'codeModelMode': True,
                'agentMode': {},
                'trendingAgentMode': {},
                'isMicMode': False,
                'userSystemPrompt': None,
                'maxTokens': self.config.max_tokens,
                'playgroundTopP': None,
                'playgroundTemperature': None,
                'isChromeExt': False,
                'githubToken': '',
                'clickedAnswer2': False,
                'clickedAnswer3': False,
                'clickedForceWebSearch': False,
                'visitFromDelta': False,
                'mobileClient': False,
                'userSelectedModel': model.value,
                'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
                'imageGenerationMode': False,
                'webSearchModePrompt': self.config.web_search_mode_prompt,
                'deepSearchMode': self.config.deep_search_mode,
            }
            
            response = self.scraper.post(
                f"{self.base_url}/chat",
                headers=self._get_headers(),
                json=data,
                stream=True,
                timeout=self.config.timeout
            )
            
            streaming_response = ""
            for value in response.iter_lines(decode_unicode=True, chunk_size=1000):
                if value:
                    streaming_response += value + '\n'
                    if prints:
                        print(value)
                        
            if response.status_code == 200:
                return {'streaming_response': streaming_response}
            raise APIRequestError(f"Chat request failed with status code: {response.status_code}")
        except Exception as e:
            raise APIRequestError(f"Chat request failed: {str(e)}")
        
    def chat(self, query: str, model: str = "GPT_4O", prints: bool = True) -> Dict[str, Any]:
        """
        Initiates a chat session with the specified model and query, returning the response and sources.
        
        This method sends a chat request to the server with the provided query and model. It then processes the response, including any sources that might be available. The method returns a dictionary containing the chat response and sources.
        
        Args:
            query (str): The user's query string.
            model (str, optional): The model to use for the chat session. Defaults to "GPT_4O".
            prints (bool, optional): A flag indicating whether to print the response. Defaults to True.
        
        Returns:
            Dict[str, Any]: A dictionary containing the chat response and sources.
        
        Raises:
            ModelNotFoundError: If the specified model is not a valid ChatModel.
            APIRequestError: If the API request fails.
        """
        try:
            chat_model = ChatModel[model.upper()]
        except KeyError:
            raise ModelNotFoundError(
                f"Invalid model: {model}. Available models: {', '.join([m.name for m in ChatModel])}"
            )
        
        response_dict = {}
        
        # Start chat request first
        chat_response = self._send_chat_request(query, chat_model, prints)
        
        # Run sources request in background
        with ThreadPoolExecutor() as executor:
            sources_future = executor.submit(self._send_sources_request, query)
            
            if 'error' not in chat_response:
                response_dict.update(sources_future.result())
            response_dict.update(chat_response)
        
        return response_dict

# Simple usage example
if __name__ == "__main__":
    # Create a chat client with default configuration
    chat = BlackBoxChat()
    
    try:
        # Send a query
        response = chat.chat("What is artificial intelligence?")
        
        # Print results
        print(f"\nResponse: {response['streaming_response']}")
        print(f"Sources: {response.get('sources', 'No sources found')}")
    except BlackBoxError as e:
        print(f"Error occurred: {str(e)}")