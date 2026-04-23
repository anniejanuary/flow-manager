from .task_registry import TaskRegistry
from .task_logic import fetch_data_task, process_data_task, store_data_task


# Auto-registration on import
TaskRegistry.register("task1", fetch_data_task)
TaskRegistry.register("task2", process_data_task)
TaskRegistry.register("task3", store_data_task)