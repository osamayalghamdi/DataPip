from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, model_validator
from loguru import logger

from app.llm import LLM
from app.schema import ROLE_TYPE, AgentState, Memory, Message, Agent, AgentCall, AgentResult, Tool, ToolCall, ToolResult


class BaseAgent(BaseModel, ABC):
    """Abstract base class for managing agent state and execution.

    Provides foundational functionality for state transitions, memory management,
    and a step-based execution loop. Subclasses must implement the `step` method.
    """

    # Core attributes
    name: str = Field(..., description="Unique name of the agent")
    description: Optional[str] = Field(None, description="Optional agent description")

    # Prompts
    system_prompt: Optional[str] = Field(
        None, description="System-level instruction prompt"
    )
    next_step_prompt: Optional[str] = Field(
        None, description="Prompt for determining next action"
    )

    # Dependencies
    llm: LLM = Field(default_factory=LLM, description="Language model instance")
    memory: Memory = Field(default_factory=Memory, description="Agent's memory store")
    state: AgentState = Field(
        default=AgentState.IDLE, description="Current agent state"
    )

    # Execution control
    max_steps: int = Field(default=10, description="Maximum steps before termination")
    current_step: int = Field(default=0, description="Current step in execution")

    duplicate_threshold: int = 2

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"  # Allow extra fields for flexibility in subclasses

    @model_validator(mode="after")
    def initialize_agent(self) -> "BaseAgent":
        """Initialize agent with default settings if not provided."""
        if self.llm is None or not isinstance(self.llm, LLM):
            self.llm = LLM(config_name=self.name.lower())
        if not isinstance(self.memory, Memory):
            self.memory = Memory()
        return self

    @asynccontextmanager
    async def state_context(self, new_state: AgentState):
        """Context manager for safe agent state transitions.

        Args:
            new_state: The state to transition to during the context.

        Yields:
            None: Allows execution within the new state.

        Raises:
            ValueError: If the new_state is invalid.
        """
        if not isinstance(new_state, AgentState):
            raise ValueError(f"Invalid state: {new_state}")

        previous_state = self.state
        self.state = new_state
        try:
            yield
        except Exception as e:
            self.state = AgentState.ERROR  # Transition to ERROR on failure
            raise e
        finally:
            self.state = previous_state  # Revert to previous state

    def update_memory(
        self,
        role: ROLE_TYPE,  # type: ignore
        content: str,
        **kwargs,
    ) -> None:
        """Add a message to the agent's memory.

        Args:
            role: The role of the message sender (user, system, assistant, tool).
            content: The message content.
            **kwargs: Additional arguments (e.g., tool_call_id for tool messages).

        Raises:
            ValueError: If the role is unsupported.
        """
        message_map = {
            "user": Message.user_message,
            "system": Message.system_message,
            "assistant": Message.assistant_message,
            "tool": lambda content, **kw: Message.tool_message(content, **kw),
        }

        if role not in message_map:
            raise ValueError(f"Unsupported message role: {role}")

        msg_factory = message_map[role]
        msg = msg_factory(content, **kwargs) if role == "tool" else msg_factory(content)
        self.memory.add_message(msg)

    async def run(self, arguments: Dict[str, Any]) -> AgentResult:
        """Run the agent with the given arguments."""
        try:
            agent_call = AgentCall(arguments=arguments)
            return await self._call(agent_call)
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            return AgentResult(success=False, error=str(e))

    @abstractmethod
    async def _call(self, agent_call: AgentCall) -> AgentResult:
        """Execute the agent's main logic."""
        pass

    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name with the given arguments."""
        try:
            # Find the tool
            tool = next((t for t in self.available_tools if t.name == tool_name), None)
            if not tool:
                return ToolResult(success=False, error=f"Tool {tool_name} not found")

            # Create tool call
            tool_call = ToolCall(name=tool_name, arguments=arguments)

            # Execute the tool
            logger.info(f"Executing tool: {tool_name}")
            result = await self._execute_tool_call(tool_call)
            
            if result.success:
                logger.info(f"Tool {tool_name} executed successfully")
            else:
                logger.error(f"Tool {tool_name} failed: {result.error}")
            
            return result

        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return ToolResult(success=False, error=str(e))

    async def _execute_tool_call(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call."""
        try:
            # Find the tool
            tool = next((t for t in self.available_tools if t.name == tool_call.name), None)
            if not tool:
                return ToolResult(success=False, error=f"Tool {tool_call.name} not found")

            # Execute the tool
            return await tool._call(tool_call)

        except Exception as e:
            logger.error(f"Error executing tool call: {str(e)}")
            return ToolResult(success=False, error=str(e))

    def handle_stuck_state(self):
        """Handle stuck state by adding a prompt to change strategy"""
        stuck_prompt = "\
        Observed duplicate responses. Consider new strategies and avoid repeating ineffective paths already attempted."
        self.next_step_prompt = f"{stuck_prompt}\n{self.next_step_prompt}"
        logger.warning(f"Agent detected stuck state. Added prompt: {stuck_prompt}")

    def is_stuck(self) -> bool:
        """Check if the agent is stuck in a loop by detecting duplicate content"""
        if len(self.memory.messages) < 2:
            return False

        last_message = self.memory.messages[-1]
        if not last_message.content:
            return False

        # Count identical content occurrences
        duplicate_count = sum(
            1
            for msg in reversed(self.memory.messages[:-1])
            if msg.role == "assistant" and msg.content == last_message.content
        )

        return duplicate_count >= self.duplicate_threshold

    @property
    def messages(self) -> List[Message]:
        """Retrieve a list of messages from the agent's memory."""
        return self.memory.messages

    @messages.setter
    def messages(self, value: List[Message]):
        """Set the list of messages in the agent's memory."""
        self.memory.messages = value

    async def __call__(self, tool_call: ToolCall) -> ToolResult:
        """Execute the tool."""
        return await self._call(tool_call)
