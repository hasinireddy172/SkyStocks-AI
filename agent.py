from dotenv import load_dotenv
load_dotenv()
import json
import requests
import subprocess
from google import genai

# =========================
# CONFIG
# =========================
import os
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# TOOLS
# =========================

def get_weather(city: str):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"

        return "Failed to fetch weather data."

    except Exception as e:
        return str(e)


def get_stock_price(symbol: str):
    try:
        url = (
            "https://www.alphavantage.co/query"
            "?function=GLOBAL_QUOTE"
            f"&symbol={symbol}"
            f"&apikey={ALPHA_VANTAGE_API_KEY}"
        )

        response = requests.get(url, timeout=15)
        data = response.json()

        if "Global Quote" not in data:
            return f"No stock data found for {symbol}"

        quote = data["Global Quote"]

        if not quote:
            return f"No stock data found for {symbol}"

        return json.dumps({
            "symbol": quote.get("01. symbol"),
            "price": quote.get("05. price"),
            "change": quote.get("09. change"),
            "change_percent": quote.get("10. change percent"),
            "volume": quote.get("06. volume"),
            "latest_trading_day": quote.get("07. latest trading day")
        })

    except Exception as e:
        return str(e)


def run_command(cmd: str):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            return result.stdout

        return result.stderr

    except Exception as e:
        return str(e)


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "get_stock_price": get_stock_price
}

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are a helpful AI Assistant.

You operate in four steps:

1. plan
2. action
3. observe
4. output

Rules:
- Return ONLY valid JSON.
- Do not use markdown.
- Do not use ```json.
- Do not add explanations outside JSON.
- Perform only ONE step at a time.
- Wait for observation after action.

JSON formats:

{
  "step":"plan",
  "content":"reasoning"
}

{
  "step":"action",
  "function":"tool_name",
  "input":"tool_input"
}

{
  "step":"output",
  "content":"final answer"
}

Available Tools:

1. get_weather(city)
2. run_command(command)
3. get_stock_price(symbol)

Tool Usage Examples:

{
  "step":"action",
  "function":"get_stock_price",
  "input":"AAPL"
}
"""

# =========================
# MAIN AGENT FUNCTION
# =========================

def run_agent(query):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": query
        }
    ]

    while True:

        try:

            prompt = ""

            for msg in messages:
                prompt += f"{msg['role']}: {msg['content']}\n"

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            assistant_response = response.text

            assistant_response = assistant_response.replace(
                "```json", ""
            )
            assistant_response = assistant_response.replace(
                "```", ""
            )
            assistant_response = assistant_response.strip()

            parsed_response = json.loads(
                assistant_response
            )

            step = parsed_response.get("step")

            # PLAN
            if step == "plan":

                messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

                continue

            # ACTION
            elif step == "action":

                tool_name = parsed_response.get(
                    "function"
                )

                tool_input = parsed_response.get(
                    "input"
                )

                if tool_name not in available_tools:
                    return "Tool not found."

                tool_output = available_tools[
                    tool_name
                ](tool_input)

                messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

                messages.append({
                    "role": "user",
                    "content": json.dumps({
                        "step": "observe",
                        "output": tool_output
                    })
                })

                continue

            # OUTPUT
            elif step == "output":

                return parsed_response.get(
                    "content"
                )

            else:

                return "Invalid response from model."

        except json.JSONDecodeError:

            return f"Model returned invalid JSON:\n\n{assistant_response}"

        except Exception as e:

            return f"Error: {str(e)}"
