import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

class InvoiceModel(BaseModel):
    total: float = Field(..., description='The final total amount of the invoice.')
    recipient: str = Field(..., description='The recipient of the invoice.')
    total: float = Field(..., description='The final total amount of the invoice.')

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

pdf = client.files.upload(file='invoice.pdf')

prompt = """
Extract the incvoice recipient name and invoice total.
Return ONLY JSON that matches the provided schema.
"""

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents=[pdf, prompt],
    config={
        "response_mime_type": "application/json",
        "response_schema": InvoiceModel
    },
)

invoice = InvoiceModel.model_validate_json(response.text)

print(invoice.model_dump())