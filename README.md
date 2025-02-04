# AI ReAct Agent

A Streamlit-based web application that implements a ReAct (Reasoning and Acting) agent using LangChain and OpenAI. The agent can search information, fetch stock market data, and get weather updates.

## Features

- Interactive chat interface using Streamlit
- ReAct agent implementation with LangChain
- Integration with multiple APIs:
  - Tavily Search
  - Alpha Vantage (stock market data)
  - WeatherAPI (weather information)
  - OpenAI GPT-3.5 Turbo

## Prerequisites

- Python 3.8+
- OpenAI API key
- LangChain API key
- Tavily API key
- Alpha Vantage API key
- WeatherAPI key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ferrerallan/ai-react-agent.git
cd ai-react-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Fill in your API keys:
```
OPENAI_API_KEY=your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=your_project
TAVILY_API_KEY=your_key
ALPHA_VANTAGE_KEY=your_key
WEATHERAPI_KEY=your_key
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run run.py
```

## Project Structure

- `run.py`: Main application entry point with Streamlit interface
- `nodes.py`: Defines agent reasoning engine and tool execution
- `react.py`: Implements ReAct agent and tools (stock data, weather)
- `state.py`: Defines agent state management

## Available Tools

1. **Stock Market Data**
   - Fetches intraday stock data with 5-minute intervals
   - Provides open, high, low, close prices and volume

2. **Weather Information**
   - Gets current weather conditions for any city
   - Shows temperature, conditions, and wind information

3. **Web Search**
   - Performs web searches using Tavily API
   - Returns relevant search results
