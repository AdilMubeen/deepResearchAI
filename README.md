# Deep Research AI Agent

A multi-LLM research agent that conducts comprehensive due diligence investigations on individuals, analyzing risk across financial, legal, reputational, association, integrity, and operational dimensions. The system orchestrates GPT-4 for query generation and report synthesis, Perplexity for real-time web search, Claude for risk analysis, and Gemini for entity extraction—producing detailed risk assessment reports with confidence scores.

## Requirements

- Python 3.10+
- API keys for: Azure OpenAI, Anthropic, Google Gemini, Perplexity

## Setup

1. Clone and navigate to the project:
```bash
cd deep-research-agent
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

5. Add your API keys to `.env`:
```
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
ANTHROPIC_API_KEY=your_key
GEMINI_API_KEY=your_key
PERPLEXITY_API_KEY=your_key
```

## Usage

### Web Interface

```bash
python app.py
```
Open http://localhost:5001

### Command Line

```bash
python main.py --target "Elizabeth Holmes" --depth 5
```

Options:
- `--target` (required): Person to research
- `--context`: Additional context
- `--focus`: Specific focus areas
- `--time-period`: Time range
- `--industry`: Industry/sector
- `--location`: Geographic location
- `--depth`: Search iterations (default: 5)

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Search    │────▶│   Extract   │────▶│    Risk     │
│  (GPT-4 + │     │  (Gemini)   │     │  (Claude)   │
│  Perplexity)│     └─────────────┘     └──────┬──────┘
└─────────────┘                                │
      ▲                                        ▼
      │                               ┌────────────────┐
      └───── loop if depth < max ─────│  depth < max?  │
                                      └────────┬───────┘
                                               │ no
                                               ▼
                                      ┌─────────────┐
                                      │   Report    │
                                      │  (GPT-4)  │
                                      └─────────────┘
```

## Output

- Risk scores (0-100) across 6 categories
- Weighted total risk score
- Entity extraction (people, organizations, timeline)
- Comprehensive markdown report
- PDF export

## Project Structure

```
├── app.py          # Flask web server
├── agent.py        # LangGraph workflow
├── models.py       # LLM clients
├── tools.py        # Search tools
├── prompts.py      # Prompt templates
├── config.py       # Configuration
├── main.py         # CLI entry point
├── templates/      # HTML templates
├── static/         # CSS/JS assets
└── requirements.txt
```

