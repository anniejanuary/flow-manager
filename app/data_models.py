from pydantic import BaseModel


class TaskDef(BaseModel):
    """
    A task definition represents a single unit of work in a workflow. It includes the name of the task and a description
        of what the task does.
    """
    name: str
    description: str


class ConditionDef(BaseModel):
    """
    A condition definition represents the logic that determines the flow of execution based on the outcome of a task.
    """
    name: str
    description: str
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str


class FlowDef(BaseModel):
    """
    A flow definition represents the entire workflow, including its unique identifier, name, starting task, list of
        tasks, and conditions that govern the flow between tasks.
    """
    id: str
    name: str
    start_task: str
    tasks: list[TaskDef]
    conditions: list[ConditionDef]


class FlowRequest(BaseModel):
    """
    A flow request represents the payload received from the API endpoint, which includes the flow definition that needs
        to be executed.
    """
    flow: FlowDef
