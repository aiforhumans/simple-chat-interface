import gradio as gr
from chat import ChatClient

chat_client = ChatClient()

def get_response(message, history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})
    
    response = chat_client.complete(messages)
    return response.content

def update_settings(temperature, model):
    chat_client.default_model = model
    return f"Settings updated: Temperature={temperature}, Model={model}"

# Create the chat interface
chat_interface = gr.ChatInterface(
    fn=get_response,
    type="messages",
    autofocus=False,
    title="Chat Assistant",
    description="Ask me anything!"
)

# Create the settings interface
settings_interface = gr.Interface(
    fn=update_settings,
    inputs=[
        gr.Slider(minimum=0, maximum=1, value=0.7, label="Temperature"),
        gr.Dropdown(
            choices=["llama2", "mistral", "gpt4all"],
            value="llama2",
            label="Model"
        )
    ],
    outputs="text",
    title="Settings",
    description="Adjust your chat settings here"
)

# Create the tabbed interface
demo = gr.TabbedInterface(
    [chat_interface, settings_interface],
    ["Chat", "Settings"]
)

if __name__ == "__main__":
    demo.launch(share=True)

