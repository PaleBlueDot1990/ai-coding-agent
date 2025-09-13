import os 
import sys 
import constants
from dotenv import load_dotenv
from google import genai 
from google.genai import types
from functions.filesinfo import schema_get_files_info
from functions.filescontent import schema_get_file_content
from functions.writefile import schema_write_file
from functions.runpyfile import schema_run_python_file
from functions.callfunction import call_function

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

    # user prompt for which model will generate answer 
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        )
    ]

    # tools that llm model can use to generate response 
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    # configurations for llm-model (system prompt and tools)
    config = types.GenerateContentConfig(
        system_instruction=constants.system_prompt,
        tools=[available_functions],
    )

    for _ in range(0,20):
        response = client.models.generate_content (
            model=constants.model_name, 
            contents=messages,
            config=config
        )

        if response.text and not response.function_calls:
            print(response.text)
            break 

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call_part=function_call, verbose=verbose)
                function_response = function_call_result.parts[0].function_response.response
                message = types.Content(
                    role="user",
                    parts=[types.Part(text=str(function_response))]
                )
                messages.append(message)
    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
