# BlackBox Chat Client

A Python client for interacting with BlackBox AI's chat models in an educational context. This client provides a simple interface to explore and understand how AI chat APIs work.

## 📝 Description

The BlackBox Chat Client is a Python library that demonstrates how to interact with AI chat models programmatically. It provides a clean, object-oriented interface for sending queries and receiving responses, making it an excellent educational resource for understanding API interactions and async programming patterns.

## ⚠️ Important Disclaimer

This code is provided **STRICTLY FOR EDUCATIONAL PURPOSES ONLY**. It is designed to help students and developers understand:
- How API clients work
- Implementation of chat interfaces
- Handling of streaming responses
- Concurrent programming patterns
- Error handling in network requests

**NOT FOR PRODUCTION USE**: This code should not be used in production environments or for any commercial purposes. It is not officially endorsed by or affiliated with BlackBox AI.

**RESPONSIBLE USAGE**: Users must:
- Respect BlackBox AI's terms of service
- Not abuse or overload their servers
- Not use this code for any malicious purposes
- Obtain proper authorization before accessing any API endpoints

## 🚀 Features

- Support for multiple AI models (GPT-4, Gemini Pro, Claude, etc.)
- Concurrent processing of requests
- Streaming response handling
- Built-in error handling and type safety
- Configurable settings
- Source verification for responses
- Simple and intuitive interface

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/sujalrajpoot/blackbox-chat-client.git
cd blackbox-chat-client
```

2. Install required dependencies:
```bash
pip install cloudscraper
```

## 📖 Usage

### Basic Usage

```python
from blackbox_chat import BlackBoxChat

# Create a chat instance
chat = BlackBoxChat()

# Send a query
try:
    response = chat.chat("What is artificial intelligence?")
    print(f"Response: {response['streaming_response']}")
    print(f"Sources: {response.get('sources', 'No sources found')}")
except Exception as e:
    print(f"Error: {str(e)}")
```

### Advanced Configuration

```python
from blackbox_chat import BlackBoxChat, ChatConfig

# Configure custom settings
config = ChatConfig(
    max_tokens=2048,
    deep_search_mode=True,
    web_search_mode_prompt=True,
    timeout=60,
    prints=True
)

# Create chat instance with custom config
chat = BlackBoxChat(config)

# Use a specific model
response = chat.chat(
    "Explain quantum computing",
    model="GPT_4O"
)
```

## 🔧 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| max_tokens | Maximum tokens in response | 1024 |
| deep_search_mode | Enable deep search | True |
| web_search_mode_prompt | Enable web search | True |
| timeout | Request timeout in seconds | 30 |
| prints | Print streaming responses | True |

## 📚 Available Models

- `GPT_4O`: GPT-4 Optimized
- `GEMINI_PRO`: Google's Gemini Pro
- `CLAUDE_SONNET_35`: Anthropic's Claude 3.5 Sonnet
- `BLACKBOX_AI_PRO`: BlackBox AI Pro
- `BLACKBOX_AI`: Standard BlackBox AI

## 🔍 Error Handling

The client includes custom error types for better error handling:

```python
try:
    response = chat.chat("your query")
except ModelNotFoundError as e:
    print("Invalid model specified:", e)
except APIRequestError as e:
    print("API request failed:", e)
except BlackBoxError as e:
    print("General error:", e)
```

## 📋 Requirements

- Python 3.7+
- cloudscraper
- concurrent.futures (standard library)
- typing (standard library)
- dataclasses (standard library)
- enum (standard library)

## 🔮 Future Improvements

- Add async/await support
- Implement rate limiting
- Add unit tests
- Add logging system
- Create command-line interface
- Add support for conversation history
- Implement retry mechanism
- Add proxy support

## 🚫 Known Limitations

- Rate limits may apply
- Response times may vary
- Some models may be unavailable
- API endpoints may change
- Not suitable for production use

## 📞 Support

For educational queries about this code:
- Open an issue on GitHub
- Contact the maintainers
- Check the documentation

Remember: This is an educational project. For production applications, please use official APIs and SDKs.

## 🙏 Acknowledgments

- Thanks to the open-source community
- Educational resources and documentation
- Contributors and maintainers

---

**Remember**: This code is for educational purposes only. Use responsibly and ethically.

---

Created with ❤️ by **Sujal Rajpoot**

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
