# GPT-5.4 Text Summarization with Reasoning Effort

A Python console app that summarizes text files using a GPT-5.4 model hosted in Azure AI Foundry, with `reasoning_effort` set to `high` via the Responses API.

## Prerequisites

- Python 3.10+
- An Azure AI Foundry resource with a GPT-5.4 model deployed
- Azure CLI installed and signed in (`az login`) for Microsoft Entra ID authentication

## Setup

1. **Create and activate a virtual environment:**

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Copy the sample env file and fill in your values:

   ```powershell
   cp .env.sample .env
   ```

   Edit `.env` with your Azure AI Foundry endpoint and model deployment name:

   ```
   AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1
   MODEL_DEPLOYMENT_NAME=gpt-5.4
   ```

4. **Sign in to Azure:**

   ```powershell
   az login
   ```

## Usage

```powershell
python summarize.py <path-to-text-file>
```

**Example:**

```powershell
python summarize.py sample.txt
```

The app will print the summary followed by token usage statistics (input, output, and reasoning tokens).

## How It Works

- Reads text from the specified file
- Authenticates to Azure using `DefaultAzureCredential` (Microsoft Entra ID)
- Calls the OpenAI Responses API (`client.responses.create()`) with `reasoning_effort` set to `high`
- Prints the plain-text summary and token usage breakdown
