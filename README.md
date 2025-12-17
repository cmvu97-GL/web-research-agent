# Simple AI Research Agent

A minimal AI agent that uses Google Gemini and web search to answer questions.

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
$ python simple_agent.py "How does gravity work?"

[SEARCH] Searching for: How does gravity work?
[SEARCH] Searching DuckDuckGo for: 'How does gravity work?'
[SEARCH] Found 3 results
[FOUND] 3 sources

[AI] Generating answer...

ANSWER:
Gravity is described as a fundamental physical interaction that derives primarily from mass. According to this physical law, every object with mass attracts every other object in the universe in proportion to each mass and inversely proportional to the square of the distance between them [2].

Different theories explain how gravity works:
*   **Newton's Theory** describes gravity as a force [1].
*   **Einstein's Theory** explains gravity as a distortion of space-time [1].
*   **Modern Physics** offers additional views, exploring gravity as a particle, a wave, or even an emergent phenomenon arising from deeper, quantum-level information, rather than a fundamental force [1, 3]. Approaches like Loop Quantum Gravity (LQG) are also being explored in the context of quantum gravity [3].
```

---
