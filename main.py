import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MODEL, SYSTEM_PROMPT

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
    
    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(model=MODEL, contents=messages, config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()