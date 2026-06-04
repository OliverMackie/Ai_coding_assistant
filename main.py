import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from function_call import *
import sys


def main():
    parser = argparse.ArgumentParser(description="Ai_agent")
    parser.add_argument("user_input", type=str, help="Parse user input string")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    function_results = []

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_input)] )
        ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Api key not found")

    client = genai.Client(api_key=api_key)
    for z in range(20):
        content = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]),)
        if content.candidates:
            candidates = content.candidates
            for candidate in candidates:
                messages.append(candidate)
        if content != None: 
            if args.verbose:
                print(f"User prompt: {args.user_input}")
                print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        #print(content.text)
            if (content.function_calls != None) and len(content.function_calls) > 0:
                for function_call in content.function_calls:
                    function_call_result = call_function(function_call, args.verbose)
                    if not function_call_result.parts:
                        raise Exception(f"Error: function call {function_call} failed")
                    if not function_call_result.parts[0].function_response:
                        raise Exception(f"Error: no function_response field for {function_call}")
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception(f"Error: no response from function {function_call}")
                    function_results.append(function_call_result.parts[0])
                    messages.append(types.Content(role="user", parts=function_results))
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                print(f"{content.text}")
                break
        else:
            raise Exception("API request failed")
        if z == 19:
            print(f"maximum iterations exceeded")
            sys.exit(1)
    

        
    
    
    


if __name__ == "__main__":
    main()
