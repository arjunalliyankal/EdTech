
import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential




endpoint = "https://models.inference.ai.azure.com"
model_name = "DeepSeek-V3-0324"
token =  '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'#os.getenv("AZURE_DEEPSEEK_API_KEY")
# token = "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"
def deep_seek_ai(dom_content, parse_description):
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )
    dom_content= dom_content[0]
    response = client.complete(
        messages=[
            SystemMessage("""You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text
 
                        """),

 
            UserMessage(parse_description),
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=10000,
        model=model_name
    )

    return response.choices[0].message.content



   