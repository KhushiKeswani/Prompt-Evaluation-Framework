import os
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('api_key')
client = genai.Client(api_key=api_key)
def ask_ai(prompt):
    response = client.models.generate_content(model = 'gemini-3.5-flash',config=types.GenerateContentConfig(
                    temperature = 0.2,
                    system_instruction="""

                    You are a STRICT evaluator.

Deduct points for:
- unnecessary words
- explanations when not asked
- hedging
- formatting issues
- verbosity
- missing information
- grammar
- tone mismatch

Do NOT give 10 unless the answer is nearly perfect.

Most good answers should score between 6 and 9.

Reply ONLY as JSON.

{
  "score": <1-10>,
  "reason": "..."
}
                    """),contents = prompt)
    usage = response.usage_metadata
    return response.text,usage