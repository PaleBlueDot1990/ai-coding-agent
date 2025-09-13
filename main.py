import os 
import sys 
from typing import List, Optional

import constants
from dotenv import load_dotenv
from google import genai 
from google.genai import types

# Tool schema imports (these are definitions of the tools the model may call)
from functions.filesinfo import schema_get_files_info
from functions.filescontent import schema_get_file_content
from functions.writefile import schema_write_file
from functions.runpyfile import schema_run_python_file
from functions.callfunction import call_function



def main():
    """
    Main function:
    - loads the GEMINI_API_KEY from environment,
    - constructs the initial user message from argv,
    - iteratively calls the model (allowing function/tool calls),
    - prints the first plain-text response returned by the model.
    """

    # Load environment variables (GEMINI_API_KEY expected)
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("GEMINI_API_KEY not found in environment. Set it and retry.")
    
    # Initialize client with the API key 
    client = genai.Client(api_key=gemini_api_key) 

    # Command-line arguments: script <user_prompt> [--verbose]
    arguments : List[str] = sys.argv
    if len(arguments) == 1:
        print("user prompt not provided!")
        return 
    user_prompt = arguments[1]

    # Verbose flag (optional)
    verbose : bool = False 
    if len(arguments) >= 3 and arguments[2] == "--verbose":
        verbose = True 

    # Initial messages, seeded with user's prompt 
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        )
    ]

    # Tools that the model can use to generate response 
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    # Configurations passed to the model: system prompt and available tools
    config = types.GenerateContentConfig(
        system_instruction=constants.system_prompt,
        tools=[available_functions],
    )

    try:
        final_respone = make_iterative_llm_calls(client, messages, config, verbose)
        print_response(final_respone, user_prompt, verbose)
    except Exception as e:
        print(f"Something went wrong- {e}")



def make_iterative_llm_calls(
    client : genai.Client,
    messages : list[types.Content], 
    config : types.GenerateContentConfig,
    verbose : bool,
):
    """
    Helper function:
    - Iteratively call the model, allowing it to call tools and update the conversation.
    - We cap iterations to avoid infinite loops in case tools keep being invoked.
    - The reponse is returned back when no more tools are to be invoked.
    """
    MAX_ITERATIONS = 20 
    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content (
            model=constants.model_name, 
            contents=messages,
            config=config
        )

        # If model returned a plain text response (and no function/tool calls), print and finish.
        if response.text and not response.function_calls:
            return response

        # Append all returned candidate contents to the conversation history.
        # Candidates are usually content parts the model proposes 
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # If the model asked to call a tool/function, invoke it and append its results to the messages.
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call_part=function_call, verbose=verbose)
                function_call_response = function_call_result.parts[0].function_response.response
                message = types.Content(
                    role="user",
                    parts=[types.Part(text=str(function_call_response))]
                )
                messages.append(message)



def print_response(response : types.GenerateContentConfig, user_prompt : str, verbose : bool):
    """
    Helper function:
    - prints the final response returned by the model
    - if verbose flag is set, then also prints the user_prompt and token usage info
    """
    print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
