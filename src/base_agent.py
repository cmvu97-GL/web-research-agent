"""
Base Agent Class
================
Simple foundation for building agents without AI.
Uses rule-based logic instead of AI reasoning.
"""

from typing import Dict, List, Callable, Any


class BaseAgent:
    """
    Simple agent framework using basic logic (no AI).

    WHY THIS EXISTS:
    - Provides structure for building agents
    - Manages tools and execution
    - Tracks what the agent has done

    SIMPLE APPROACH:
    - No AI decision-making
    - Uses straightforward rules
    - Easy to understand and customize
    """

    def __init__(self, tools: Dict[str, Callable] = None):
        """
        Initialize the agent.

        Args:
            tools: Dictionary of available tools
                   Example: {'search': search_web, 'fetch': fetch_webpage}
        """
        self.tools = tools or {}
        self.history = []  # Remember what we've done

        print(f"[AGENT] Initialized with {len(self.tools)} tools")
        if self.tools:
            print(f"[AGENT] Available: {', '.join(self.tools.keys())}")

    def add_tool(self, name: str, function: Callable):
        """Add a new tool the agent can use."""
        self.tools[name] = function
        print(f"[AGENT] Added tool: {name}")

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool and return result.

        WHY THIS METHOD:
        - Centralizes tool execution
        - Records what was done
        - Handles errors
        """
        if tool_name not in self.tools:
            error = f"Tool '{tool_name}' not found"
            print(f"[ERROR] {error}")
            return {'success': False, 'error': error}

        print(f"[AGENT] Using {tool_name}...")

        try:
            result = self.tools[tool_name](**kwargs)

            # Remember what we did
            self.history.append({
                'tool': tool_name,
                'args': kwargs,
                'result': result
            })

            return result

        except Exception as e:
            error = f"Tool failed: {str(e)}"
            print(f"[ERROR] {error}")
            return {'success': False, 'error': error}

    def get_history(self) -> List[Dict]:
        """Get everything the agent has done."""
        return self.history

    def reset(self):
        """Clear history and start fresh."""
        self.history = []
        print("[AGENT] Reset complete")
