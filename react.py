from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI
import requests
import os

load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")


@tool
def get_intraday_data(symbol: str) -> str:
   """
   Fetches intraday stock data from Alpha Vantage API.
   
   :param symbol: Stock symbol
   :return: Recent intraday stock data
   """
   api_key = os.getenv("ALPHA_VANTAGE_KEY")
   
   if not api_key:
       return "Error: Alpha Vantage API key not found"
   
   params = {
       "function": "TIME_SERIES_INTRADAY",
       "symbol": symbol,
       "interval": "5min",
       "apikey": api_key,
       "outputsize": "compact"
   }
   
   try:
       response = requests.get("https://www.alphavantage.co/query", params=params)
       data = response.json()
       print("***** FINANCE TOOL *****")

       if "Error Message" in data:
           return f"Error: {data['Error Message']}"
       
       time_series = data.get("Time Series (5min)", {})
       if not time_series:
           return "No data found"
       
       
       latest_date = list(time_series.keys())[0]
       latest_data = time_series[latest_date]
       
    #    print(latest_data)
       return f"Intraday data for {symbol} ({latest_date}):\n" + \
              f"Open: ${latest_data['1. open']}\n" + \
              f"High: ${latest_data['2. high']}\n" + \
              f"Low: ${latest_data['3. low']}\n" + \
              f"Close: ${latest_data['4. close']}\n" + \
              f"Volume: {latest_data['5. volume']}"
   
   except Exception as e:
       return f"Error fetching data: {str(e)}"
    
@tool
def get_marilia_biscuit(query: str) -> str:
    """
    Use this tool to identify if a biscuit is categorized as biscoito,bolacha or treco
    
    :param query: Description of the biscuit including its ingredients (e.g., "biscoito feito de farinha")
    :return: Classification as 'biscoito', 'bolacha' or 'treco'
    """
    try:
        print("***** MARILIA BISCUIT *****")
        query = query.lower()
                
        words = query.split()
        item = next((word for word in words if word in ["biscoito", "bolacha", "biscoite"]), "item")
        
        if "farinha" in query:
            return f"{item} is a biscoito"
        elif "fuba" in query:
            return f"{item} is a bolacha"
        elif "milho" in query:
            return f"{item} is a treco"
        else:
            return f"Cannot determine if it is biscoito or bolacha without ingredient information"
    
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_weather_data(city: str) -> str:
    """
    Fetches current weather data from Weather API
    
    :param city: City name to get weather data
    :return: Current weather conditions
    """
    api_key = os.getenv("WEATHERAPI_KEY")
    
    if not api_key:
        return "Error: Weather API key not found"
        
    params = {"key": api_key, "q": city, "aqi": "no"}
    
    try:
        response = requests.get("http://api.weatherapi.com/v1/current.json", params=params)
        data = response.json()

        print("***** WEATHER TOOL *****")
        
        
        if "error" in data:
            return f"Error: {data['error']['message']}"
        # print(data["location"])
        location = data["location"]
        current = data["current"]
        condition = current["condition"]
        
        return f"Weather in {location['name']}, {location['country']}: {condition['text']}, {current['temp_c']}°C, Wind: {current['wind_kph']} km/h {current['wind_dir']}"

    except Exception as e:
        return f"Error: {str(e)}"

tools = [TavilySearchResults(max_results=1), get_intraday_data, get_weather_data, get_marilia_biscuit]

llm = ChatOpenAI(model="gpt-4")

react_agent_runnable = create_react_agent(llm, tools, react_prompt)
