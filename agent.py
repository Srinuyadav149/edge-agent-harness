import pathlib


class SystemInstruction:
    def __init__(
        self,
        persona: str,
        objective: str,
        instructions: list[str],
        examples: list[str],
        tool_schemas: list[str]
    ):
        self.persona: str = persona
        self.objective: str = objective
        self.instructions: list[str] = instructions
        self.examples: list[str] = examples
        self.tool_schemas: list[str] = tool_schemas

    def __str__(self) -> str:
        string_list = []
        string_list.append("# Persona")
        string_list.append(f"{self.persona}")
        string_list.append("# Objective")
        string_list.append(f"{self.objective}")
        string_list.append("# Instructions")
        string_list.append("".join(f"* {instruction}\n" for instruction in self.instructions))
        string_list.append("# Examples")
        string_list.append("".join(f"* {example}\n" for example in self.examples))
        string_list.append("# Tool Schemas")
        string_list.append("".join(f"* {tool_schema}\n" for tool_schema in self.tool_schemas))
        return "\n\n".join(string_list)

class GuardRail:
    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        severity: int,
        guardrail: str,
        positive_examples: list[str],
        negative_examples: list[str]
    ):
        self.id: int = id
        self.name: str = name
        self.type: str = type
        self.severity: int = severity
        self.guardrail: str = guardrail
        self.positive_examples: list[str] = positive_examples
        self.negative_examples: list[str] = negative_examples

    def __str__(self) -> str:
        string_list = []
        string_list.append(f"# GuardRail({self.id})")
        string_list.append(f"* id: {self.id}")
        string_list.append(f"* name: {self.name}")
        string_list.append(f"* type: {self.type}")
        string_list.append(f"* severity: {self.severity}/5")
        string_list.append("## Guardrail")
        string_list.append(f"{self.guardrail}")
        string_list.append("## Positive Examples")
        string_list.append("".join(f"* {example}\n" for example in self.positive_examples))
        string_list.append("## Negative Examples")
        string_list.append("".join(f"* {example}\n" for example in self.negative_examples))
        return "\n\n".join(string_list)

class Memory:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        type: str,
        importance: int,
        memory: str,
        related_memories: list[int]
    ):
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.type: str = type
        self.importance: int = importance
        self.memory: str = memory
        self.related_memories: list[int] = related_memories
        
    def __str__(self) -> str:
        string_list = []
        string_list.append(f"# Memory({self.id})")
        string_list.append(f"* id: {self.id}")
        string_list.append(f"* name: {self.name}")
        string_list.append(f"* description: {self.description}")
        string_list.append(f"* type: {self.type}")
        string_list.append(f"* importance: {self.importance}/5")
        string_list.append("## Memory")
        string_list.append(f"{self.memory}")
        string_list.append("## Related Memories")
        string_list.append("".join(f"* Memory({id})\n" for id in self.related_memories))
        return "\n\n".join(string_list)

class Task:
    def __init__(
                 self,
                 id: int,
                 name: str,
                 description: str,
                 priority: int,
                 is_completed: bool,
                 sub_tasks: list[int]
             ):
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.priority: int = priority
        self.is_completed: bool = is_completed
        self.sub_tasks: list[int] = sub_tasks

    def __str__(self) -> str:
        string_list = []
        string_list.append(f"# Task({self.id})")
        string_list.append(f"* id: {self.id}")
        string_list.append(f"* name: {self.name}")
        string_list.append(f"* description: {self.description}")
        string_list.append(f"* priority: {self.priority}/5")
        string_list.append(f"* is_completed: {self.is_completed}")
        string_list.append("## Sub Tasks")
        string_list.append("".join(f"* Task({id})\n" for id in self.sub_tasks))
        return "\n\n".join(string_list)

class History:
    def __init__(
                 self,
                 global_sequence_id: int,
                 local_sequence_id: int,
                 status: str,
                 input_tokens: str,
                 reasoning_tokens: str,
                 output_tokens: str,
                 tool_call_output: str
             ):
        self.global_sequence_id: int = global_sequence_id
        self.local_sequence_id: int = local_sequence_id
        self.status: str = status
        self.input_tokens: str = input_tokens
        self.reasoning_tokens: str = reasoning_tokens
        self.output_tokens: str = output_tokens
        self.tool_call_output: str = tool_call_output

    def __str__(self) -> str:
        string_list = []
        string_list.append(f"# History({self.global_sequence_id}: {self.local_sequence_id})")
        string_list.append(f"* global_sequence_id: {self.global_sequence_id}")
        string_list.append(f"* local_sequence_id: {self.local_sequence_id}")
        string_list.append(f"* status: {self.status}")
        string_list.append("## Input Tokens")
        string_list.append(f"{self.input_tokens}")
        string_list.append("## Reasoning Tokens")
        string_list.append(f"{self.reasoning_tokens}")
        string_list.append("## Output Tokens")
        string_list.append(f"{self.output_tokens}")
        string_list.append("## Tool Call Output")
        string_list.append(f"{self.tool_call_output}")
        return "\n\n".join(string_list)

class Permission:
    def __init__(
                 self,
                 id: int,
                 path: str | pathlib.Path,
                 read: bool=False,
                 write: bool=False,
                 execute: bool=False,
                 read_recursive: bool=False,
                 write_recursive: bool=False,
                 execute_recursive: bool=False
             ):
        self.id = id
        self.path: pathlib.Path = pathlib.Path(path).resolve()
        self.read: bool = read
        self.write: bool = write
        self.execute: bool = execute
        self.read_recursive: bool = read_recursive
        self.write_recursive: bool = write_recursive
        self.execute_recursive: bool = execute_recursive

    def __str__(self) -> str:
        string_list = []
        string_list.append(f"# Permission({self.id})")
        string_list.append("## Path")
        string_list.append(f"{self.path}")
        string_list.append("## Direct Permissions")
        string_list.append(f"* read: {self.read}")
        string_list.append(f"* write: {self.write}")
        string_list.append(f"* execute: {self.execute}")
        string_list.append("## Recursive Permissions")
        string_list.append(f"* read: {self.read_recursive}")
        string_list.append(f"* write: {self.write_recursive}")
        string_list.append(f"* execute: {self.execute_recursive}")
        return "\n\n".join(string_list)

class Agent:
    def __init__(
                 self,
                 agent_id: int,
                 name: str,
                 description: str
             ):
        self.agent_id: int = agent_id
        self.name: str = name
        self.description: str = description
        self.system_instruction: SystemInstruction
        self.guard_rails: list[dict] = []
        self.memory: list[dict] = []
        self.tasks: list[Task] = []
        self.history: list[History] = []
        self.permissions: list[Permission] = []

