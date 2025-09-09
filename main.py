import os 
import sys 
import constants
from dotenv import load_dotenv
from google import genai 
from google.genai import types

def main():
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key) 

    arguments = sys.argv
    if len(arguments) == 1:
        print("user prompt not provided!")
        return 
    user_prompt = arguments[1]

    verbose = False 
    if len(arguments) >= 3 and arguments[2] == "--verbose":
        verbose = True 

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        )
    ]

    response = client.models.generate_content (
        model=constants.model_name, 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=constants.system_prompt)
    )

    if not verbose:
        print(response.text)
    else:
        print(response.text)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
