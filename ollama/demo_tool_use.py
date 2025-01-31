from ollama import ChatResponse, chat
from pprint import pprint

MODEL = "llama3.2:1b"


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
      a (int): The first number
      b (int): The second number

    Returns:
      int: The sum of the two numbers
    """
    a = int(a)
    b = int(b)
    return a + b


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """
    a = int(a)
    b = int(b)
    return a - b


# Tools can still be manually defined and passed into chat
subtract_two_numbers_tool = {
    "type": "function",
    "function": {
        "name": "subtract_two_numbers",
        "description": "Subtract two numbers",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": "The first number"},
                "b": {"type": "integer", "description": "The second number"},
            },
        },
    },
}

available_functions = {
    "add_two_numbers": add_two_numbers,
    "subtract_two_numbers": subtract_two_numbers,
}

questions = [
    {"role": "user", "content": "What is three plus one?"},
    {"role": "user", "content": "And what is 42 minus eight?"},
]

response = None
messages = []

for question in questions:
    print(f">> Question: {question['content']}")

    messages.append(question)
    got_answer = False

    while not got_answer:
        print(">> messages=")
        pprint(messages)
        response: ChatResponse = chat(
            MODEL,
            messages=messages,
            tools=[add_two_numbers, subtract_two_numbers_tool],
        )
        assert response is not None, "Must have response."
        print(">> response.message=")
        pprint(response.message)
        if response.message.tool_calls:
            # There may be multiple tool calls in the response
            tool_results = []
            for tool in response.message.tool_calls:
                # Ensure the function is available, and then call it
                if function_to_call := available_functions.get(tool.function.name):
                    output = function_to_call(**tool.function.arguments)
                    tool_results.append(
                        {
                            "role": "tool",
                            "content": str(output),
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
