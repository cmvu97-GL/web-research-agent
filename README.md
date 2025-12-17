# Web Research Agent

A Python-based web research agent that uses Google Search API and web scraping to gather information automatically.

**Perfect for learning how agents work!** No AI required - uses simple, understandable logic.

---

## 🎯 What This Agent Does

1. **Searches Google** - Uses Google Custom Search API to find relevant websites
2. **Fetches Webpages** - Downloads and reads webpage content
3. **Extracts Information** - Cleans HTML and extracts readable text
4. **Organizes Results** - Presents findings in a structured format

---

## 📁 Project Structure

```
web-research-agent/
├── src/                           # Source code
│   ├── __init__.py               # Makes src a Python package
│   ├── tools.py                  # Web scraping tools (fetch, extract, search)
│   ├── base_agent.py             # Base agent framework
│   └── simple_research_agent.py  # Simple research agent (no AI)
├── main.py                        # Example usage script
├── requirements.txt               # Python dependencies
├── .env                          # API keys (you need to create this!)
└── README.md                     # This file
```

---

## 🚀 Setup Instructions

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - For downloading webpages
- `beautifulsoup4` - For parsing HTML
- `lxml` - Fast HTML parser
- `google-api-python-client` - Google Custom Search API
- `python-dotenv` - For loading environment variables

### Step 2: Create `.env` File

Create a file called `.env` in the project root with your API keys:

```
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=60610a6ebcbae449d
```

**How to get these:**

**Google API Key:**
1. Go to https://console.cloud.google.com/apis/credentials
2. Create a new API key
3. Enable "Custom Search API"

**Google CSE ID:**
- You already have this: `60610a6ebcbae449d`

### Step 3: Run the Agent

```bash
python main.py
```

---

## 📖 How to Use the Agent

### Quick Search (Just Google Snippets)

```python
from src.simple_research_agent import SimpleResearchAgent

agent = SimpleResearchAgent()

# Fast search - just shows Google results
result = agent.quick_search("What is Python?")
print(result)
```

### Full Research (Fetches and Reads Webpages)

```python
from src.simple_research_agent import SimpleResearchAgent

agent = SimpleResearchAgent()

# Deep research - actually reads webpages
result = agent.research(
    question="What is Python used for?",
    num_sources=2  # Check 2 websites
)

print(result['summary'])
```

---

## 🧠 Understanding the Code

### 1. Tools (The "Hands" - `src/tools.py`)

Individual capabilities the agent can use:

**`search_web(query)`**
- Searches Google using the Custom Search API
- Returns: List of URLs, titles, snippets

**`fetch_webpage(url)`**
- Downloads a webpage from the internet
- Returns: HTML content

**`extract_text(html)`**
- Converts HTML to clean, readable text
- Removes ads, scripts, navigation

**`extract_links(html, base_url)`**
- Finds all links on a webpage
- Converts relative URLs to absolute

### 2. Base Agent (The "Framework" - `src/base_agent.py`)

Provides structure for all agents:

**Key Features:**
- **Tool Management** - Register and execute tools
- **History Tracking** - Remember what the agent did
- **Error Handling** - Gracefully handle failures

**Example:**
```python
agent = BaseAgent(tools={'search': search_web})
result = agent.execute_tool('search', query="Python")
```

### 3. Research Agent (The "Brain" - `src/simple_research_agent.py`)

Specialized agent for web research:

**How It Works:**
```
User Question → Google Search → Fetch Webpages → Extract Text → Organize Results
```

**Two Modes:**

1. **Quick Search** - Fast, only Google snippets
2. **Full Research** - Slow, reads full webpages

---

## 💡 Learning Path

### Beginner: Understanding the Tools

Start by playing with individual tools:

```python
from src import tools

# Try searching
results = tools.search_web("Python programming")
print(results)

# Try fetching a webpage
page = tools.fetch_webpage("https://python.org")
print(page['status_code'])  # Should be 200

# Try extracting text
text = tools.extract_text(page['content'])
print(text[:500])  # First 500 characters
```

### Intermediate: Understanding the Agent

Explore how the agent uses tools:

```python
from src.simple_research_agent import SimpleResearchAgent

agent = SimpleResearchAgent()

# Do a research task
result = agent.research("What is machine learning?")

# Check what the agent did
for action in agent.get_history():
    print(f"Tool used: {action['tool']}")
```

### Advanced: Build Your Own Agent

Create a specialized agent:

```python
from src.base_agent import BaseAgent
from src import tools

class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__({
            'search': tools.search_web,
            'fetch': tools.fetch_webpage,
            'extract_text': tools.extract_text
        })

    def get_latest_news(self, topic):
        # Search for news
        results = self.execute_tool('search', query=f"{topic} news")

        # Fetch top article
        page = self.execute_tool('fetch', url=results[0]['url'])
        text = self.execute_tool('extract_text', html=page['content'])

        return text

# Use it
news_agent = NewsAgent()
article = news_agent.get_latest_news("AI")
print(article)
```

---

## 🎓 Key Concepts Explained

### What is an Agent?

An **agent** is a program that:
1. **Perceives** its environment (searches, fetches data)
2. **Acts** using tools (calls functions)
3. **Works toward a goal** (answer the question)

**Your agent:**
- **Goal:** Answer research questions
- **Perception:** Google search results
- **Actions:** Fetch pages, extract text

### What is a Tool?

A **tool** is a specific capability:
- One tool = one function
- Tools are independent and reusable
- Agent decides which tools to use

**Examples:**
- `search_web()` = Tool for searching
- `fetch_webpage()` = Tool for downloading
- `extract_text()` = Tool for cleaning HTML

### Agent vs Script

**Script (simple):**
```python
results = search_web("Python")
page = fetch_webpage(results[0]['url'])
text = extract_text(page)
print(text)
```

**Agent (structured):**
```python
agent = ResearchAgent()
answer = agent.research("Python")  # Agent decides how to use tools
```

**Benefits of Agent:**
- Reusable
- Trackable (history)
- Extendable (add more tools)
- Organized

---

## 🚧 Limitations (Without AI)

This agent uses simple rules, not AI:

**❌ Cannot:**
- Understand meaning
- Synthesize information from multiple sources
- Make intelligent decisions
- Learn from experience

**✅ Can:**
- Search Google
- Fetch webpages
- Extract text
- Organize results

**To add intelligence:** Consider integrating Claude API (Anthropic) for AI reasoning.

---

## 🔧 Troubleshooting

### "GOOGLE_API_KEY not found"

**Solution:** Create a `.env` file with your Google API key

### "API quota exceeded"

**Solution:** Google Custom Search has a free tier limit (100 queries/day). Wait 24 hours or upgrade.

### "ImportError: No module named 'googleapiclient'"

**Solution:** Run `pip install -r requirements.txt`

### Webpage fetch fails (403, 404 errors)

**Solution:** Some websites block bots. Try a different URL or add more sophisticated headers.

---

## 📚 Next Steps

1. **Run the examples** - See how it works
2. **Modify `main.py`** - Try your own research questions
3. **Add new tools** - Create custom capabilities
4. **Build a specialized agent** - News agent, price tracker, etc.
5. **Add AI** - Integrate Claude or GPT for true intelligence

---

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new tools
- Create specialized agents
- Improve error handling
- Add documentation

---

## 📄 License

Open source - use it to learn and build!

---

## 🙋 Questions?

**Q: Why no AI/Claude?**
A: Simpler to learn! Add AI later when you understand the basics.

**Q: Can I use a different search API?**
A: Yes! Just replace `search_web()` in `tools.py`

**Q: How do I add more capabilities?**
A: Create new functions in `tools.py` and add them to the agent

**Q: What's next after this?**
A: Try adding AI (Claude/GPT) for intelligent reasoning and synthesis
