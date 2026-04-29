import json
from openai import OpenAI
from llm_discovery.core.config import settings

llm_model = "gpt-3.5-turbo"
llm_client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)

def classify_samples_with_llm(column_name: str, samples: list):
    # create a prompt for the LLM to classify the data samples into PII categories
    prompt = f"""
    Analyze the following data samples from a database column named '{column_name}'.
    Determine the probability distribution that this data belongs to the following PII categories:
    1. Email Address
    2. Phone Number
    3. Social Security Number (SSN)
    4. Credit Card Number
    5. National ID Number
    6. Full Name
    7. First Name
    8. Last Name / Surname
    9. TCKN (Turkish Citizenship Number)
    10. Home Address
    11. Date of Birth
    12. IP Address
    13. None / Other

    Data Samples:
    {json.dumps(samples)}

    Return ONLY a JSON object mapping the category names to a probability float between 0.0 and 1.0. The sum of probabilities should equal 1.0.
    """
    
    # call the LLM API to get the classification probabilities as required format
    response = llm_client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": "You are a data classification API."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    
    return json.loads(response.choices[0].message.content)