import requests
from groq import Groq

#  Correct API key and URL
GROQ_API_KEY = ""  # Create a groq API key and place it to "".
client = Groq(api_key=GROQ_API_KEY)

def convert_natural_language_to_sql(user_query):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Use an available model like llama3-8b-8192 or llama3-70b-8192
            messages=[
                {"role": "system", "content": (
                    "You are a helpful AI assistant that converts natural language to SQL queries. "
                    "Return only a valid SQL query without any explanation or extra text."
                )},
                {"role": "user", "content": f"Convert this to SQL: {user_query}"}
            ],
            temperature=0.2,
            max_tokens=100
        )

        
        sql_query = response.choices[0].message.content.strip()

        #  Remove markdown formatting if present
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        return sql_query

    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    
    
