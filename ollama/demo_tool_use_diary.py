from ollama import ChatResponse, chat
from pprint import pprint

from typing import List

import os
from typing import Dict

# MODEL = "llama3.2:1b"
MODEL = "llama3.2:3b"
# MODEL = "granite3.1-dense:2b"
# MODEL = "granite3.1-dense:8b"
# MODEL = "smollm2:1.7b"
# MODEL = "command-r7b"

NOTES_PATH = os.path.join(os.path.dirname(__file__), 'notes')
REMEMBER_NOTE = os.path.join(os.path.dirname(__file__), 'remember.txt')


def list_files() -> List[str]:  
    """
    List available note files.

    Returns:
        List[str]: A list of filenames available in the NOTES_PATH directory.
    """
    return [f for f in os.listdir(NOTES_PATH) if os.path.isfile(os.path.join(NOTES_PATH, f))]


def read_file(filename: str) -> str:
    """
    Read the content of a given note file.

    Args:
        filename (str): The name of the file to read. (Not the full path)

    Returns:
        str: The content of the file.
    """
    file_path = os.path.join(NOTES_PATH, filename)
    if not os.path.isfile(file_path):
        return f"File {filename} does not exist in the notes directory. The following files exist: {list_files()}"
    
    with open(file_path, 'r') as file:
        return file.read()
    

def search_file(term: str) -> Dict[str, str]:
    """
    Search for a term in all note files.

    Args:
        term (str): The term to search for.

    Returns:
        Dict[str, str]: A dictionary where keys are filenames and values are lines containing the term.
    """
    results = {}
    for filename in list_files():
        file_path = os.path.join(NOTES_PATH, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            matching_lines = [line.strip() for line in lines if term in line]
            if matching_lines:
                results[filename] = matching_lines
    return results


def remember(entry: str):
    """
    Save a new entry to a note file that you as assistant may use to remember things across sessions.

    Args:
        entry (str): The content to save in the note file.
    """
    with open(REMEMBER_NOTE, 'a') as file:
        file.write(f"{entry}\n")

def recall_all_memories() -> List[str]:
    """
    Recall all entries from the remember note file.

    Returns:
        List[str]: A list of all entries in the remember note file.
    """
    if not os.path.isfile(REMEMBER_NOTE):
        return []

    with open(REMEMBER_NOTE, 'r') as file:
        return [line.strip() for line in file.readlines()]


available_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "search_file": search_file,
    "remember": remember,
    "recall_all_memories": recall_all_memories,
}

questions = [
    {"role": "system", "content": "You have to help the user explore their diary. These are their personal notes for a couple of days. You can read the list of available notes and access the content of individual notes. The note files are named in a YY-MM-DD.md pattern. Make sure you understand in which order these files are meant to be. You may use `read_file` with any of the available files in order to assist the user. You may also search the notes for terms. Additionally you have the ability to remember and recall information between conversations with the user. Make sure you recall all memories before the first interaction." + "\n\n# Available tools:\n" + "\n".join(
        ["## " + n + "\n" + f.__doc__ for n, f in available_functions.items()]
    )},
    {"role": "user", "content": "Is there something you remember from previous conversations we had?"},
    {"role": "user", "content": "Please list the available files"},
    {"role": "user", "content": "Please find all the days I talk about the Mandy or Charlotte"},
    {"role": "user", "content": "Please summarize what happened with the girls in order. I am confused."},
    {"role": "user", "content": "Who should I spend the rest of my life with, then?"},
    {"role": "user", "content": "Make sure you remember that for next time ..."}
]

response = None
messages = []

for question in questions:
    messages.append(question)
    got_answer = False

    while not got_answer:
        print(">> messages=")
        pprint(messages)
        response: ChatResponse = chat(
            MODEL,
            messages=messages,
            tools=list(available_functions.values())
        )
        assert response is not None, "Must have response."
        print(">> response.message=")
        pprint(response.message)
        messages.append(response.message.model_dump())
        if response.message.tool_calls:
            # There may be multiple tool calls in the response
            tool_results = []
            for tool in response.message.tool_calls:
                # Ensure the function is available, and then call it
                if function_to_call := available_functions.get(tool.function.name):
                    try:
                      if 'properties' in tool.function.arguments:
                         args = tool.function.arguments['properties']
                      else:
                         args = tool.function.arguments
                      output = function_to_call(**args)
                      tool_results.append(
                          {
                              "role": "tool",
                              "content": str(output),
                              "name": tool.function.name,
                          }
                      )
                    except Exception as e:
                      tool_results.append(
                          {
                              "role": "tool",
                              "content": str(e),
                              "name": tool.function.name,
                          }
                      )
                else:
                    print("  Function", tool.function.name, "not found")
            print(">> tool_results=")
            pprint(tool_results)
            messages.extend(tool_results)
            print("=" * 40)
        else:  # No tool calls needed
          got_answer = True
