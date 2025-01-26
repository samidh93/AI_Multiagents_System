import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log the loading of environment variables
logging.info('Loading environment variables from .env')
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OPENAI_API_KEY is not set in the .env file.")
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")

# Log the successful loading of the API key
logging.info('Successfully loaded OPENAI_API_KEY')

# 2) Import relevant functionality
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import Tool
from langchain_openai import ChatOpenAI

# Log the initialization of the tools
logging.info('Initializing tools')

# 3) Define custom tool functions
def research_tool(query: str) -> str:
    logging.info(f'Researching topic: {query}')
    research_data = {
        "AI": "Artificial Intelligence is the simulation of human intelligence in machines.",
        "LangChain": "LangChain is an open-source framework for building AI applications.",
        "AI Agents": "AI Agents are self-contained systems that perform tasks. They are used to build more complex systems."
    }
    result = research_data.get(query, "No information found.")
    logging.info(f'Research result for {query}: {result}')
    return result

def summarizer_tool(content: str) -> str:
    logging.info('Summarizing content')
    bullet_points = content.replace(". ", ".\n- ")
    result = "Summary:\n- " + bullet_points
    logging.info('Summarization result: ' + result)
    return result

def save_as_txt_tool(content: str, filename: str = "output.txt") -> str:
    logging.info(f'Saving content to {filename}')
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    result = f"Text saved successfully as '{filename}'."
    logging.info(result)
    return result

# 4) Wrap each function in a langchain_community Tool
research = Tool(
    name="research",
    func=research_tool,
    description="Use this tool to research a given topic."
)

summarizer = Tool(
    name="summarizer",
    func=summarizer_tool,
    description="Use this tool to summarize text into bullet points."
)

save_as_txt = Tool(
    name="save_as_txt",
    func=lambda x: save_as_txt_tool(x),  
    description="Use this tool to save the provided text to a .txt file. (Argument=content only)"
)

tools = [research, summarizer, save_as_txt]

# 5) Create an LLM and the agent
logging.info('Creating LLM and agent')
memory = MemorySaver()
llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4" if you have access
    temperature=0,
    openai_api_key=openai_api_key
)

# Log agent creation
logging.info('Agent created successfully')

agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory
)

# 6) Stream the agent’s output with user messages
config = {"configurable": {"thread_id": "abc123"}}

# Example 1: Greet the agent
logging.info('Sending first user message')
print("---- FIRST USER MESSAGE ----")
user_message_1 = "Hi, I'm Bob and I live in San Francisco."
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=user_message_1)]},
    config
):
    logging.info('Received response from agent')
    print(chunk)
    print("----")

# Example 2: Prompt agent to research, summarize, and save output
logging.info('Sending second user message')
print("\n---- SECOND USER MESSAGE ----")
user_message_2 = (
    "Research about AI Agents, then summarize it into bullet points, and finally use "
    "the save_as_txt tool to write your summary to a text file."
)
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=user_message_2)]},
    config
):
    logging.info('Received response from agent')
    print(chunk)
    print("----")
