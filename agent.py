import pathlib
from enum import Flag


class PermissionFlag(Flag):
    READ = 1
    WRITE = 2
    EXECUTE = 4
    READ_RECURSIVE = 8
    WRITE_RECURSIVE = 16
    EXECUTE_RECURSIVE = 32


class SystemInstruction:
    def __init__(
        self,
        persona: str,
        objective: str,
        instructions: list[str],
        examples: list[str],
        tool_schemas: list[str]
    ) -> None:
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
    ) -> None:
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
        related_memories: set[int]
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.type: str = type
        self.importance: int = importance
        self.memory: str = memory
        self.related_memories: set[int] = related_memories
        
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

class MemoryManager:
    def __init__(self) -> None:
        self.memories: dict[int, Memory] = {}

    def add(self, memory: Memory) -> str | None:
        retrieved_memory: Memory | None = self.memories.get(memory.id, None)
        if retrieved_memory is not None:
            return ""
        self.memories[memory.id] = memory

    def set_relation(self, source_memory_id: int, related_memory_id: int, bidirectional: bool = False) -> str | None:
        source_memory: Memory | None = self.memories.get(source_memory_id, None)
        related_memory: Memory | None = self.memories.get(related_memory_id, None)
        if source_memory is None:
            return f"Error: Source Memory with id:({source_memory_id}) not found."
        if related_memory is None:
            return f"Error: Related Memory with id:({related_memory_id}) not found."
        source_memory.related_memories.add(related_memory_id)
        if bidirectional:
            related_memory.related_memories.add(source_memory_id)

    def get(self, memory_id: int) -> Memory | str:
        memory: Memory | None = self.memories.get(memory_id, None)
        if memory is None:
            return f"Error: Memory with id:({memory_id} not found.)"
        return memory

    def get_related(self, memory_id: int) -> tuple[Memory, list[Memory]] | str:
        memory: Memory | None = self.memories.get(memory_id, None)
        if memory is None:
            return f"Error: Memory with id:({memory_id}) not found."
        return (memory, [self.memories[memory_id] for memory_id in self.memories])

class Task:
    def __init__(
                 self,
                 id: int,
                 name: str,
                 description: str,
                 priority: int,
                 is_completed: bool,
                 sub_tasks: set[int]
             ) -> None:
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.priority: int = priority
        self.is_completed: bool = is_completed
        self.sub_tasks: set[int] = sub_tasks

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

class TaskManager:
    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}

    def add(self, task: Task) -> str | None:
        retrieved_task: Task | None = self.tasks.get(task.id, None)
        if retrieved_task is not None:
            return f"Error: Task with id:({task.id}) already exists."
        self.tasks[task.id] = task
    
    def set_sub_task(self, parent_task_id: int, sub_task_id: int) -> str | None:
        parent_task: Task | None = self.tasks.get(parent_task_id, None)
        sub_task: Task | None = self.tasks.get(sub_task_id, None)
        if parent_task is None:
            return f"Error: Parent Task with id:({parent_task_id}) not found."
        if sub_task is None:
            return f"Error: Sub Task with id:({sub_task_id}) not found."
        parent_task.sub_tasks.add(sub_task_id)

    def get(self, task_id: int) -> Task | str:
        task: Task | None = self.tasks.get(task_id, None)
        if task is None:
            return f"Error: Task with id:({task_id}) not found."
        return task

    def get_sub_tasks(self, task_id: int) -> tuple[Task, list[Task]] | str:
        task: Task | None = self.tasks.get(task_id, None)
        if task is None:
            return f"Error: Task with id:({task_id}) not found."
        return (task, [self.tasks[id] for id in self.tasks])
        
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
             ) -> None:
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
                 flag: PermissionFlag
             ) -> None:
        self.id = id
        self.path: pathlib.Path = pathlib.Path(path).resolve()
        if PermissionFlag.READ_RECURSIVE in flag and PermissionFlag.READ not in flag:
            raise ValueError("ValueError: Recursive Read Permission cannot be granted without having Read Permission")
        if PermissionFlag.WRITE_RECURSIVE in flag and PermissionFlag.WRITE not in flag:
            raise ValueError("ValueError: Recursive Write Permission cannot be granted without having Write Permission")
        if PermissionFlag.EXECUTE_RECURSIVE in flag and PermissionFlag.EXECUTE not in flag:
            raise ValueError("ValueError: Recursive Execute Permission cannot be granted without having Execute Permission")
        self.flag: PermissionFlag = flag

    def __str__(self) -> str:
        string_list = []
        string_list.append(f"# Permission({self.id})")
        string_list.append("## Path")
        string_list.append(f"{self.path}")
        string_list.append("## Direct Permissions")
        string_list.append(f"* read: {PermissionFlag.READ in self.flag}")
        string_list.append(f"* write: {PermissionFlag.WRITE in self.flag}")
        string_list.append(f"* execute: {PermissionFlag.EXECUTE in self.flag}")
        string_list.append("## Recursive Permissions")
        string_list.append(f"* read: {PermissionFlag.READ_RECURSIVE in self.flag}")
        string_list.append(f"* write: {PermissionFlag.WRITE_RECURSIVE in self.flag}")
        string_list.append(f"* execute: {PermissionFlag.EXECUTE_RECURSIVE in self.flag}")
        return "\n\n".join(string_list)

class PermissionManager:
    def __init__(self) -> None:
        self.permissions: dict[int, Permission] = {}

    def add(self, permission: Permission) -> str | None:
        retrieved_permission: Permission | None = self.permissions.get(permission.id, None)
        if retrieved_permission is not None:
            return f"Error: Permission with id({permission.id}) already exists."
        self.permissions[permission.id] = permission

    def remove(self, permission_id: int) -> str | None:
        permission: Permission | None  = self.permissions.get(permission_id, None)
        if permission is None:
            return f"Error: Permission with id({permission_id}) does not exists."
        self.permissions.pop(permission_id)

    def grant(self, permission_id: int, flag: PermissionFlag) -> str | None:
        permission: Permission | None  = self.permissions.get(permission_id, None)
        if permission is None:
            return f"Error: Permission with id({permission_id}) does not exists."
        try:
            permission.flag |= flag
        except ValueError as ve:
            raise ValueError(ve)
    
    def withdraw(self, permission_id: int, flag: PermissionFlag) -> str | None:
        permission: Permission | None  = self.permissions.get(permission_id, None)
        if permission is None:
            return f"Error: Permission with id({permission_id}) does not exists."
        try:
            permission.flag &= ~flag
        except ValueError as ve:
            raise ValueError(ve)

class Agent:
    def __init__(
                 self,
                 agent_id: int,
                 name: str,
                 description: str
             ) -> None:
        self.agent_id: int = agent_id
        self.name: str = name
        self.description: str = description
        self.system_instruction: SystemInstruction
        self.guard_rails: list[dict] = []
        self.memory_manager: MemoryManager = MemoryManager()
        self.task_manager: TaskManager = TaskManager()
        self.history: list[History] = []
        self.permissions: PermissionManager = PermissionManager()

