import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from function_call import available_functions


def main():
    parser = argparse.ArgumentParser(description="Ai_agent")
    parser.add_argument("user_input", type=str, help="Parse user input string")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_input)] )
        ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise Exception("Api key not found")

    client = genai.Client(api_key=api_key)
    content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]),)

    if content != None: 
        if args.verbose:
            print(f"User prompt: {args.user_input}")
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        print(content.text)
        if (content.function_calls != None) and len(content.function_calls) > 0:
            for function_call in content.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        raise Exception("API request failed")
    
    


if __name__ == "__main__":
    main()
