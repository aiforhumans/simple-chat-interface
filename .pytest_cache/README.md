# Simple Chat Interface

A simple chat interface built with Gradio that supports multiple language models.

## Features
- Chat interface with message history
- Configurable settings (temperature, model selection)
- Support for multiple models (llama2, mistral, gpt4all)
- Local API compatibility with LM Studio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aiforhumans/simple-chat-interface.git
cd simple-chat-interface
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export LM_STUDIO_API_KEY=your-key
export LM_STUDIO_BASE_URL=http://localhost:1234/v1
```

## Usage

Run the application:
```bash
python gradio_app.py
```

The interface will be available at `http://localhost:7860`

## Configuration
- Temperature: Controls response randomness (0-1)
- Model: Choose between available models (llama2, mistral, gpt4all)

## Development
To run tests:
```bash
pytest
```

## License
MIT

## Author
[aiforhumans](https://github.com/aiforhumans)
