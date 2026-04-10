import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():
    parser = argparse.ArgumentParser(
        description="Summarize text from a file using GPT-5.4 on Azure AI Foundry with high reasoning effort."
    )
    parser.add_argument("file", help="Path to the text file to summarize.")
    args = parser.parse_args()

    # Load configuration from .env
    load_dotenv()
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.4")

    if not endpoint:
        print("Error: AZURE_OPENAI_ENDPOINT is not set. Configure it in the .env file.")
        sys.exit(1)

    # Read the input file
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    if not text.strip():
        print("Error: The input file is empty.")
        sys.exit(1)

    # Authenticate with Microsoft Entra ID
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )

    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider,
    )

    print(f"Sending {len(text)} characters to {model} with reasoning_effort=high ...\n")

    # Call the Responses API with high reasoning effort
    response = client.responses.create(
        model=model,
        instructions="You are a helpful assistant that produces clear, concise summaries of the provided text. Do not use markdown formatting in your response. Output plain text only.",
        input=[
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{text}",
            },
        ],
        reasoning={
            "effort": "high",
            "summary": "auto",
        },
    )

    # Extract and print the summary
    summary = response.output_text
    print("=== Summary ===")
    print(summary)

    # Print reasoning summary if available
    # for item in response.output:
    #     if item.type == "reasoning" and item.summary:
    #         print("\n=== Reasoning Summary ===")
    #         for part in item.summary:
    #             if hasattr(part, "text"):
    #                 print(part.text)

    # Print token usage
    if response.usage:
        print("\n=== Token Usage ===")
        print(f"  Input tokens:     {response.usage.input_tokens}")
        print(f"  Output tokens:    {response.usage.output_tokens}")
        if response.usage.output_tokens_details:
            print(f"  Reasoning tokens: {response.usage.output_tokens_details.reasoning_tokens}")
        print(f"  Total tokens:     {response.usage.total_tokens}")


if __name__ == "__main__":
    main()
