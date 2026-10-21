import pathlib


class SystemInstruction:
    def __init__(
        self,
        persona: str,
        objective: str,
        instructions: list[str],
        examples: list[str],
        tool_schemas: list[str],
    ):
        self.persona: str = persona
        self.objective: str = objective
        self.instructions: list[str] = instructions
        self.examples: list[str] = examples
        self.tool_schemas: list[str] = tool_schemas

class GuardRail:
    def __init__(
        self,
        guardrail_id: int,
        name: str,
        type: str,
        guardrail: str,
        positive_examples: list[str],
        negative_examples: list[str],
        severity: int
    ):
        self.guardrail_id: int = guardrail_id
        self.name: str = name
        self.type: str = type
        self.guardrail: str = guardrail
        self.positive_examples: list[str] = positive_examples
        self.negative_examples: list[str] = negative_examples
        self.severity: int = severity

class Memory:
    def __init__(
        self,
        memory_id: int,
        name: str,
        description: str,
        memory: str,
        type: str,
        importance: int
    ):
        self.memory_id: int = memory_id
        self.name: str = name
        self.description: str = description
        self.memory: str = memory
        self.type: str = type
        self.importance: int = importance
        self.related_memories: list[int] = []

class Task:
    def __init__(
                 self,
                 task_id: int,
                 name: str,
                 description: str,
                 priority: int
             ):
        self.task_id: int = task_id
        self.name: str = name
        self.description: str = description
        self.priority = priority
        self.is_completed: bool = False
        self.sub_tasks: list[int] = []

class History:
    def __init__(
                 self,
                 global_sequence_id: int,
                 local_sequence_id: int,
                 input_tokens: str,
                 reasoning_tokens: str,
                 output_tokens: str,
                 tool_call_output: str,
                 status: str
             ):
        self.global_sequence_id: int = global_sequence_id
        self.local_sequence_id: int = local_sequence_id
        self.input_tokens: str = input_tokens
        self.reasoning_tokens: str = reasoning_tokens
        self.output_tokens: str = output_tokens
        self.tool_call_output: str = tool_call_output
        self.status: str = status

class Permission:
    def __init__(
                 self,
                 path: str | pathlib.Path,
                 read: bool=False,
                 write: bool=False,
                 execute: bool=False,
                 read_recursive: bool=False,
                 write_recursive: bool=False,
                 execute_recursive: bool=False
             ):
        self.path: pathlib.Path = pathlib.Path(path).resolve()
        self.read: bool = read
        self.write: bool = write
        self.execute: bool = execute
        self.read_recursive: bool = read_recursive
        self.write_recursive: bool = write_recursive
        self.execute_recursive: bool = execute_recursive

class Agent:
    def __init__(self, name: str):
        self.name: str = name
        self.system_instruction: SystemInstruction
        self.guard_rails: list[dict] = []
        self.memory: list[dict] = []
        self.tasks: list[Task] = []
        self.history: list[History] = []
        self.permissions: list[Permission] = []

