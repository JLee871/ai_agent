import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL, MAX_ITERS
from prompt import SYSTEM_PROMPT
from call_function import available_functions, call_function

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python main.py <prompt>")
        sys.exit(1)

    verbose = False
    if args[-1] == "--verbose":
        verbose = True
        args = args[:-1]

    prompt = " ".join(args)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    if verbose:
        print(f"User prompt: {prompt}")
    
    #generate_content(client, messages, verbose)

    
    for i in range(MAX_ITERS + 1):
        if i == MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client: genai.Client, messages: list[types.Content], verbose=False):
    response = client.models.generate_content(model=MODEL, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT))
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        return response.text
    
    function_responses = []
    for call in response.function_calls:
        function_call_result = call_function(call, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception("Fatal error: something went wrong calling the function")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()