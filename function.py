import os
import json
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.env()
)

# 2. Create the Blueprint (Tell the model what function you have)
weather_tool = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather data for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name."}
                },
                "required": ["city"]
            }
        }
    }
]

# 3. Your real local Python function
def get_weather(city):
    return {"city": city, "temperature": "28°C", "condition": "Sunny"}

def run_poc():
    while True:
        city = input("\nEnter City name (or type 'exit' to quit): ").strip()
        if city.lower() in ['exit', 'quit']:
            print("Shutting down safely. Goodbye!")
            break
            
        user_input = city
        print(f"📥 User Input: '{user_input}'")

        # Send the input AND the tool blueprint to the API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"What is the weather like in {user_input}?"}],
            tools=weather_tool,
            temperature=0.0
        )

        message = response.choices[0].message

        # 4. FIXED INDENTATION: This block now runs cleanly inside the loop cycle
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            
            # Turn the JSON string arguments into a Python dictionary safely
            arguments = json.loads(tool_call.function.arguments)
            extracted_city = arguments["city"]

            print("\n🎯 LLM Tool Extraction Results:")
            print(f"🔹 Function to call: {tool_call.function.name}")
            print(f"🔹 Parameter extracted: {extracted_city}")

            # Execute your local Python function using the LLM's data
            final_output = get_weather(extracted_city)
            print(f"🔌 Run Local Function Output: {final_output}")
        else:
            print(f"\n📝 Normal Chat Text Response: {message.content}")

if __name__ == "__main__":
    run_poc()
