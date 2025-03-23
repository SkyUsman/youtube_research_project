# Vertex API Research

## Information

- Gemini API can be used in Vertex API to interact gemini-1.5-pro to generate text from text prompt.
- Provides the ability to build virtual agents (chatbots) that generate answers based on the content (website, documents) you include in data stores.

## Usage

Install Vertex AI SDK:

```
%pip install --upgrade --user google-cloud-aiplatform
```

Load in the Gemini 1.5 Pro Model and Generate a text from text prompt:

```
prompt = """Create a numbered list of 10 items. Each item in the list should be a trend in the tech industry.

Each trend should be less than 5 words."""  # try your own prompt

response = model.generate_content(prompt)

print(response.text)

```

We can also test chat prompts with multi-turn conversations.

More information can be found here: https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/gemini/getting-started/intro_gemini_python.ipynb

## Financial

- $1,000 trial credit, valid one year after signup.
- $12.00 per 1000 queries.
- More pricing listed here: https://cloud.google.com/generative-ai-app-builder/pricing
