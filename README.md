# AI_Multiagents_System
An Intro to multiagents AI system.
Key Features of This System
Multi-Agent Design:

The research agent is responsible for gathering raw information.
The summarizer agent processes the raw data into concise points.
Dynamic Decision-Making:

The system decides which agent/tool to call based on the task description.
Extensibility:

Additional tools/agents can be added for more tasks, such as:
A translator agent.
An analyzer agent.
A planner agent.

# create virtual environment
python3 -m venv venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# create a .env file
Create a .env File In the root directory of your project, create a file named .env and add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key

# run the main file
python3 main.py