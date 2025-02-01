from ollama import ChatResponse, chat
from pprint import pprint

MODEL = "llama3.2:3b"


def add_two_numbers(a: int, b: int) -> str:
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
    return f"{a} + {b} = {a+b}"


def subtract_two_numbers(a: int, b: int) -> str:
    """
    Subtract two numbers
    """
    a = int(a)
    b = int(b)
    return f"{a} - {b} = {a-b}"

available_functions = {
    "add_two_numbers": add_two_numbers,
    "subtract_two_numbers": subtract_two_numbers,
}

questions = [
    # {"role": "user", "content": "What is three plus one?"},
    # {"role": "user", "content": "And what is 42 minus eight?"},
    # {"role": "user", "content": "What is 1 and 1?"},
    # {"role": "user", "content": "If I have 10 cookies and eat 4, how many are left?"},
    {"role": "system", "content": "Assist the user as accurately as possible. You may need to call the tools more than once. For example if the user asks for the sum of 4 numbers a, b, c and d, first call the add_two_numbers tool with a and b, remember the result, then call it with c and d, remember that result and then call the toll again with the two remembered results."},
    {"role": "user", "content": "What is the sum of 20, -31, 3 and 8?"}
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
            tools=[add_two_numbers, subtract_two_numbers],
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
