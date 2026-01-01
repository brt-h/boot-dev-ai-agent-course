import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count if response.usage_metadata else 0
    response_tokens = response.usage_metadata.candidates_token_count if response.usage_metadata else 0
    response_text = response.text or "No response"
    function_calls = response.function_calls  # Can be None when empty

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if not function_calls:
        print(f"Response: {response_text}")
    else:
        list_of_function_results = []
        for func_call in function_calls:
            function_call_result = call_function(func_call, verbose=args.verbose)

            if function_call_result.parts == []:
                raise Exception("Empty parts list from call_function")
            elif function_call_result.parts[0].function_response is None:
                raise Exception("Missing function_response in parts[0]")
            elif function_call_result.parts[0].function_response.response is None:
                raise Exception("Missing response in function_response")
            else:
                list_of_function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")


if __name__ == "__main__":
    main()
