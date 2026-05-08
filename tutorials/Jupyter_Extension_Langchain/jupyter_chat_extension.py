# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Building a Chat Interface for Jupyter with LangChain
#
# This notebook shows you how to build a simple but powerful AI chat interface that lives inside Jupyter.
#
# ## What You'll Build
#
# - A chat UI using `ipywidgets`
# - LangChain integration for AI responses
# - Conversation memory management
# - Context-aware chat that can see notebook variables
#
# ## Prerequisites
#
# Make sure you have your OpenAI API key set:
#
# ```bash
# export OPENAI_API_KEY="your-key-here"
# ```

# %% [markdown]
# ## Step 1: Install Dependencies
#
# First, let's install what we need.

# %%
# Install required packages
# !pip install --upgrade langchain langchain-openai langchain-community ipywidgets python-dotenv pandas

# %% [markdown]
# ## Step 2: Import Required Libraries

# %%
import os
from ipywidgets import Textarea, Button, Output, VBox, HBox
from IPython.display import clear_output

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Verify API key
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not found")
else:
    print("API key loaded")


# %% [markdown]
# ## Step 3: Build a Basic Chat Interface
#
# Let's start with a simple version that just displays messages.


# %%
class BasicChatUI:
    """A simple chat UI using ipywidgets."""

    def _on_send(self, button):
        """Handle send button click."""
        message = self.input_box.value.strip()
        if message:
            with self.output:
                print(f"You: {message}")
                print("AI: [Response would go here]\n")
            self.input_box.value = ""  # Clear input

    def __init__(self):
        # Create widgets
        self.output = Output(
            layout={
                "border": "1px solid #ccc",
                "height": "300px",
                "overflow": "auto",
            }
        )
        self.input_box = Textarea(
            placeholder="Type your message here...",
            layout={"width": "80%", "height": "60px"},
        )
        self.send_button = Button(
            description="Send", button_style="primary", layout={"width": "18%"}
        )

        # Wire up the button
        self.send_button.on_click(self._on_send, remove=True)
        self.send_button.on_click(self._on_send)

    def display(self):
        """Display the chat interface."""
        input_row = HBox([self.input_box, self.send_button])
        return VBox([self.output, input_row])


# Test it out
basic_chat = BasicChatUI()
basic_chat.display()


# %% [markdown]
# Try typing a message and clicking Send. You'll see it appear in the output area.
#
# Now let's add the AI part!

# %% [markdown]
# ## Step 4: Add LangChain Integration
#
# Now we'll connect to LangChain to get real AI responses.


# %%
class ChatInterface:
    """A chat interface with modern LangChain (RunnableWithMessageHistory)."""

    def _on_send(self, button):
        """Handle send button click."""
        user_message = self.input_box.value.strip()
        if not user_message:
            return

        # Clear input and display user message
        self.input_box.value = ""
        with self.output:
            print(f"You: {user_message}")

        # Disable button while processing
        self.send_button.disabled = True
        self.send_button.description = "Thinking..."

        # Get response synchronously
        try:
            response = self.chain.invoke(
                [HumanMessage(content=user_message)],
                config={"configurable": {"session_id": self.session_id}},
            )

            with self.output:
                print(f"AI: {response.content}\n")

        except Exception as e:
            with self.output:
                print(f"Error: {str(e)}\n")
        finally:
            self.send_button.disabled = False
            self.send_button.description = "Send"

    def __init__(
        self, model="gpt-4o-mini", temperature=0.7, session_id="default"
    ):
        # UI components
        self.output = Output(
            layout={
                "border": "1px solid #ccc",
                "height": "400px",
                "overflow": "auto",
            }
        )
        self.input_box = Textarea(
            placeholder="Ask me anything...",
            layout={"width": "80%", "height": "60px"},
        )
        self.send_button = Button(
            description="Send", button_style="primary", layout={"width": "18%"}
        )
        self.send_button.on_click(self._on_send)

        # Session id for memory
        self.session_id = session_id

        # LangChain setup (modern)
        llm = ChatOpenAI(model=model, temperature=temperature)

        self._store = {}  # session_id -> ChatMessageHistory

        def get_session_history(sid: str):
            if sid not in self._store:
                self._store[sid] = ChatMessageHistory()
            return self._store[sid]

        self.chain = RunnableWithMessageHistory(
            llm,
            get_session_history,
        )

        # Welcome message
        with self.output:
            print("AI Assistant ready! Ask me anything.\n")

    def display(self):
        """Display the chat interface."""
        input_row = HBox([self.input_box, self.send_button])
        return VBox([self.output, input_row])


# Clear old output and create fresh chat instance
clear_output(wait=True)

chat = ChatInterface()

# Close old instance if it exists
try:
    if "chat" in globals():
        chat.output.close()
        chat.input_box.close()
        chat.send_button.close()
except:
    pass
chat.display()


# %% [markdown]
# You now have a working AI chat interface.
#
# Try asking:
# - "What is LangChain?"
# - "Explain async/await in Python"
# - "Write a haiku about Jupyter notebooks"
#
# The AI will remember the conversation, so you can have multi-turn dialogues.

# %% [markdown]
# ## Step 5: Add Context Awareness
#
# Let's make the chat aware of variables in your notebook.


# %%
class ContextAwareChatInterface(ChatInterface):
    """Chat interface that can see notebook variables."""

    def __init__(
        self,
        model="gpt-4o-mini",
        temperature=0.7,
        use_context=True,
        session_id="default",
    ):
        super().__init__(
            model=model, temperature=temperature, session_id=session_id
        )
        self.use_context = use_context

    def _get_notebook_context(self):
        """Get context from notebook variables."""
        from IPython import get_ipython

        ipython = get_ipython()

        if not ipython:
            return "No notebook context available."

        user_ns = ipython.user_ns
        context_items = []

        for name, value in user_ns.items():
            # Skip private variables and common IPython internals
            if name.startswith("_") or name in [
                "In",
                "Out",
                "get_ipython",
                "exit",
                "quit",
            ]:
                continue

            var_type = type(value).__name__

            extra_info = ""
            try:
                if var_type == "DataFrame":
                    extra_info = f" with shape {value.shape}"
                elif var_type in ["list", "tuple", "set"]:
                    extra_info = f" with {len(value)} items"
                elif var_type == "dict":
                    extra_info = f" with {len(value)} keys"
            except Exception:
                pass

            context_items.append(f"  - {name}: {var_type}{extra_info}")

        if not context_items:
            return "No user-defined variables found."

        return "Available variables:\n" + "\n".join(context_items)

    def _on_send(self, button):
        """Handle send button click with context awareness."""
        user_message = self.input_box.value.strip()
        if not user_message:
            return

        # Clear input and display user message
        self.input_box.value = ""
        with self.output:
            print(f"You: {user_message}")

        # Disable button while processing
        self.send_button.disabled = True
        self.send_button.description = "Thinking..."

        # Get response synchronously with optional context
        try:
            if self.use_context:
                context = self._get_notebook_context()
                enhanced_message = (
                    "You can use the notebook context below to answer the user.\n"
                    "If context is irrelevant, ignore it.\n\n"
                    f"Notebook context:\n{context}\n\n"
                    f"User message:\n{user_message}"
                )
            else:
                enhanced_message = user_message

            response = self.chain.invoke(
                [HumanMessage(content=enhanced_message)],
                config={"configurable": {"session_id": self.session_id}},
            )

            with self.output:
                print(f"AI: {response.content}\n")

        except Exception as e:
            with self.output:
                print(f"Error: {str(e)}\n")
        finally:
            self.send_button.disabled = False
            self.send_button.description = "Send"


# %% [markdown]
# Let's test the context-aware chat. First, create some variables:

# %%
# Create some example variables
import pandas as pd

my_list = [1, 2, 3, 4, 5]
my_dict = {"name": "Alice", "age": 30, "city": "NYC"}
df = pd.DataFrame(
    {
        "product": ["A", "B", "C"],
        "sales": [100, 200, 150],
        "region": ["East", "West", "North"],
    }
)

print("Variables created:")
print(f"  my_list: {my_list}")
print(f"  my_dict: {my_dict}")
print(f"  df:\n{df}")

# %% [markdown]
# Now create the context-aware chat:

# %%
# Clear old output and create fresh context-aware chat
from IPython.display import clear_output

clear_output(wait=True)

context_chat = ContextAwareChatInterface()

# Close old instance if it exists
try:
    if "context_chat" in globals():
        context_chat.output.close()
        context_chat.input_box.close()
        context_chat.send_button.close()
except:
    pass
context_chat.display()

# %% [markdown]
# Try asking:
# - "What variables do I have defined?"
# - "What's in my dataframe?"
# - "What is the sum of my_list?"
#
# The AI can now see your notebook variables and answer questions about them!

# %% [markdown]
# ## Summary
#
# You've learned how to:
#
# - Build a chat UI with `ipywidgets`
# - Integrate LangChain for AI responses
# - Handle async operations properly
# - Make the chat context-aware of notebook variables
#
# ## Next Steps
#
# - Package it: Turn this into a proper Jupyter extension
# - Add security: Sandbox code execution
# - Improve UX: Add markdown rendering, code highlighting
# - Multi-modal: Support image inputs
# - Persistence: Store conversations in a database
#
# The code is simple, but the possibilities are endless.
