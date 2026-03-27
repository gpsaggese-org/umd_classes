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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## 1. Setup and Initialization
# Before diving into use cases, we should initialize the notebook with the required setup:

# %%
# Import the helper script
import helpers.hopenai as hopenai

# Set up logging for debugging
import logging

logging.basicConfig(level=logging.INFO)

# Set OpenAI API key
import os
from typing import List

# %%
os.environ["OPENAI_API_KEY"] = "<your_openai_api_key>"

# %% [markdown]
# ## 1. Travel Agent chat assistant:
# #### Goal: Cretae a chat agent that will help the user to create an itinary to visit New York Trip considering all the constraints.

# %%
# Define the prompt for the travel assistant
user_prompt = """
I am visiting New York City for 3 days. Please create a detailed itinerary,
including popular attractions, food recommendations, and some evening activities.
I already booked flight tickets and hotel near Newark penn station.
Constraints:
1) Dates: from 24th to 27th Dec.
1) My budget for travel is around $400 excluding hotel and flight.
2) I am planning to travel through subway and for rest of the trip I am planning to walk.
3) Also, take into account traffic and tourist rush at popular places.
"""

# Define the system instructions for the assistant
system_instructions = """
You are a travel assistant specializing in creating personalized travel itineraries.
Your recommendations should balance sightseeing, food, and leisure activities considering provided constraints.
Provide details like the time required for activities and approximate costs where possible.
"""

# Use the get_completion method to generate the trip plan
trip_plan = hopenai.get_completion(
    user=user_prompt,
    system=system_instructions,
    model="gpt-4o-mini",
    temperature=0.7,  # Slightly increase temperature for creative outputs
)

# Print the generated trip itinerary
print("3-Day New York City Trip Itinerary:")
print(trip_plan)

# %% [markdown]
# ## 2. Chatbot for Coding Assistance
# #### Goal: Create a chatbot that assists developers with coding questions based on the provided coding style guide.

# %%
# Define the assistant name and instructions
assistant_name = "CodingAssistant"
instructions = "You are a helpful coding assistant. Answer technical questions clearly and concisely."
vector_store_name = "coding_help_vector_store"

# Provide relevant documentation files
file_paths = ["../helpers_root/docs/coding/all.coding_style.how_to_guide.md"]

# Create or retrieve the assistant
assistant = hopenai.get_coding_style_assistant(
    assistant_name=assistant_name,
    instructions=instructions,
    vector_store_name=vector_store_name,
    file_paths=file_paths,
)

# Query the assistant
question = "What are common python mistaks that I should keep in mind while writing code?"
response_messages = hopenai.get_query_assistant(assistant, question)

# Display the assistant's response
for message in response_messages:
    # Ensure the message has content to process
    if hasattr(message, "content"):
        for content_block in message.content:
            if hasattr(content_block, "text") and hasattr(
                content_block.text, "value"
            ):
                print(f"{message.role}: {content_block.text.value}")
            else:
                print(f"{message.role}: [No valid text content found]")
    else:
        print("[No content attribute in the message]")


# %% [markdown]
# ## 3. Managing Uploaded Files
# #### Goal: List, view, and delete files in the OpenAI API.


# %%
def print_file_info(files_list: List[str]) -> None:
    """
    Prints file info.
    """
    for file in files_list:
        file_info = hopenai.file_to_info(file)
        print(file_info)


# %%
# List all files
client = hopenai.OpenAI()
files_before = list(client.files.list())
print("Uploaded files:")
print_file_info(files_before)
# Delete all files (with confirmation)
hopenai.delete_all_files(ask_for_confirmation=False)
# Verify deletion
files_after = list(client.files.list())
print("Files after deletion:")
print_file_info(files_after)

# %% [markdown]
# ## 4. Batch Upload to Vector Store
# #### Goal: Add multiple files to a vector store and check their status.

# %%
# Upload files to a vector store
vector_store_name = "batch_vector_store"
file_paths = [
    "../helpers_root/docs/coding/all.imports_and_packages.how_to_guide.md",
    "../helpers_root/docs/coding/all.write_unit_tests.how_to_guide.md",
    "../helpers_root/docs/coding/all.coding_style.how_to_guide.md",
]  # Example paths

# Create or find vector store
client = hopenai.OpenAI()
vector_store = client.beta.vector_stores.create(name=vector_store_name)

# Upload files to the vector store
file_streams = [open(path, "rb") for path in file_paths]
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

# Display file batch status
print(f"File batch status: {file_batch.status}")

# %% [markdown]
# ## 5. Tasking an AI Agent to Generate Code and Unit Tests Using Coding Guides
# #### Scenario:
#
# You are a developer working on a new feature for a Python application. You uploaded documentation about best practices for imports, writing unit tests, and coding styles to a vector store. Now, you want to create an AI agent that can generate boilerplate code and its corresponding unit tests for a given functionality while adhering to these guides.

# %%
# Step 1: Create a coding assistant
assistant_name = "CodeAndTestAssistant"
instructions = (
    "You are a coding assistant trained to write Python code and unit tests."
    "Adhere strictly to the following rules based on the uploaded guide:"
    "- Adhere to PEP 8 coding standards."
    "- Use proper imports as documented in the coding guides."
    "- Write comprehensive and edge-case-aware unit tests."
)

# Create or retrieve the assistant
coding_assistant = hopenai.get_coding_style_assistant(
    assistant_name=assistant_name,
    instructions=instructions,
    vector_store_name=vector_store_name,
    file_paths=None,  # Files already uploaded to the vector store
)

# Step 2: Query the assistant to generate code and tests
task = (
    "Write a Python function `calculate_area` that computes the area of a rectangle "
    "given its width and height. Then, write unit tests to verify its functionality."
)

response_messages = hopenai.get_query_assistant(coding_assistant, task)

# Display the assistant's response
for message in response_messages:
    # Ensure the message has content to process
    if hasattr(message, "content"):
        for content_block in message.content:
            if hasattr(content_block, "text") and hasattr(
                content_block.text, "value"
            ):
                print(f"{message.role}: {content_block.text.value}")
            else:
                print(f"{message.role}: [No valid text content found]")
    else:
        print("[No content attribute in the message]")


# %% [markdown]
# ## 6. Manage assistants.
# #### Goal: List and delete existing assistants.


# %%
def print_assistant_info(assistants_list: List[str]) -> None:
    """
    Prints assistant info.
    """
    for assistant in assistants_list:
        assistant_info = hopenai.assistant_to_info(assistant)
        print(assistant_info)


# List all assistants
assistants = client.beta.assistants.list()
print("Assistants:")
print_assistant_info(assistants.data)

# Delete all assistants (with confirmation)
hopenai.delete_all_assistants(ask_for_confirmation=False)

# Verify deletion
assistants_after = client.beta.assistants.list()
print("Assistants after deletion:")
print_assistant_info(assistants_after.data)

# %%

# %%
