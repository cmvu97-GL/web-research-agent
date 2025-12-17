# Simple AI Research Agent

A minimal AI agent that uses Google Gemini and web search to answer questions.

## Requirements Met

✅ **Framework**: Google Gemini AI
✅ **Tools**: Web search (DuckDuckGo)
✅ **LLM**: Gemini 2.5 Flash

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google API Key
https://makersuite.google.com/app/apikey

### 3. Create `.env` file
```
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run
```bash
python simple_agent.py
```

---

## How It Works

```
Question → Web Search Tool → LLM (Gemini) → Answer
```

1. **Tool** searches DuckDuckGo for relevant information
2. **LLM** analyzes results and generates intelligent answer

---

## Files

- `simple_agent.py` - Main agent (85 lines)
- `src/tools.py` - Web search tool
- `requirements.txt` - Dependencies
- `.env.example` - API key template

---

## Example Output

```
$ python simple_agent.py

[SEARCH] Searching for: What is Python used for?
[FOUND] 3 sources

[AI] Generating answer...

ANSWER:
Python is used for data science, web development, automation,
natural language processing, computer vision, and scientific computing.
```

---

**That's it!** Simple agent demonstrating tool use + LLM integration.
