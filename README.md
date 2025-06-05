# Research Agent System

A system of specialized agents working together to conduct research, analyze information, and generate insights.

## Overview

This system consists of three main components:

1. **Research Coordinator**: The main agent that orchestrates the research process and manages the team
2. **Data Collector**: Specializes in gathering information from various sources
3. **Analysis Expert**: Focuses on analyzing and interpreting the collected data

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agents
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Project Structure

```
research-agent-system/
├── agents/
│   ├── root_agent.py      # Research Coordinator agent
│   └── specialist_agents.py  # Data Collector and Analysis Expert agents
├── tools/
│   ├── web_search.py      # Web search functionality using DuckDuckGo
│   ├── content_analysis.py # Text analysis using NLTK
│   ├── data_collection.py # Data collection from various sources
│   ├── summarization.py   # Research findings summarization
│   └── __init__.py        # Tool exports
├── requirements.txt
├── .env.example
└── README.md
```

## Tools

The system includes several specialized tools:

### Web Search (`web_search.py`)
- Uses DuckDuckGo API for web searches
- Returns structured search results with metadata
- Handles error cases and rate limiting

### Content Analysis (`content_analysis.py`)
- Performs sentiment analysis on text
- Extracts keywords and key phrases
- Generates text summaries
- Uses NLTK for natural language processing

### Data Collection (`data_collection.py`)
- Collects data from multiple sources:
  - Web pages (content, links, metadata)
  - APIs (REST endpoints)
  - CSV files (with statistical summaries)
  - JSON files
- Handles various data formats and error cases

### Summarization (`summarization.py`)
- Provides multiple summary formats:
  - Brief (2-sentence summary)
  - Detailed (comprehensive summary)
  - Structured (key findings, keywords, metadata)
- Uses advanced NLP techniques for summarization

## Usage

1. Start the Research Coordinator:
```python
from agents.root_agent import research_coordinator

# Initialize the coordinator
coordinator = research_coordinator

# Start a research task
result = coordinator.run("Research quantum computing applications in healthcare")
```

2. The coordinator will:
   - Break down the research task
   - Delegate to specialist agents
   - Collect and analyze information
   - Generate a comprehensive report

## Example

```python
from agents.root_agent import research_coordinator

# Example research task
task = "Analyze the impact of AI on healthcare in 2024"

# Run the research
result = research_coordinator.run(task)

# Process the results
print(result["summary"])
print(result["key_findings"])
print(result["sources"])
```
