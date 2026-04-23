from typing import Any

from app.data_models import FlowDef
from app.tasks.task_registry import TaskRegistry


class FlowEngine:
    """
    The core engine that takes a FlowDef configuration and executes it.
        It maintains a pointer to the current task and uses the conditions defined in the JSON
        to determine the next task based on the outcome of the current task's execution.
        This design allows for a highly flexible and dynamic flow control mechanism that can be
        easily modified by changing the JSON configuration without touching the engine code.
        The engine also logs each step of the execution for transparency and debugging purposes.
    """
    def __init__(self, flow_config: FlowDef):
        """
        Initializes the Flow Engine with the provided flow configuration.
        Args:
            flow_config (FlowDef): The configuration for the flow, including tasks and conditions.
        """
        self.config: FlowDef = flow_config
        self.conditions_map = {cond.source_task: cond for cond in self.config.conditions}

    def run(self) -> dict[str, Any]:
        """
        Executes the flow based on the configuration, as long as there are valid tasks to execute and the flow hasn't
            reached an "end" state.
        1. Starts at the defined starting task.
        2. Executes the task and captures its result.
        3. Evaluates the conditions to determine the next task.
        Returns:
                dict: A summary of the flow execution, including status and logs.
        """
        print(f"\n--- Starting Flow: {self.config.name} ({self.config.id}) ---")

        current_task_name = self.config.start_task
        execution_log = []

        while current_task_name and current_task_name != "end":

            # 1. Fetch the function from the dynamic registry
            try:
                task_func = TaskRegistry.get_task(current_task_name)
            except NotImplementedError as e:
                error_msg = str(e)
                execution_log.append({"task": current_task_name, "error": error_msg})
                break

            # 2. Execute the function registered for the task and get the result
            try:
                result = task_func()
                execution_log.append({"task": current_task_name, "status": result})
            except Exception as e:
                execution_log.append({"task": current_task_name, "status": "error", "message": str(e)})
                result = "error"

            # 3. Evaluate Conditions to find the next task
            condition = self.conditions_map.get(current_task_name)
            # If no condition is defined for this task, the flow ends here naturally
            if not condition:
                print(f"[Flow Manager] No routing rules found after '{current_task_name}'. Ending flow.")
                break

            print(f"[Flow Manager] Evaluating '{current_task_name}' result '{result}' against expected outcome '{condition.outcome}'")

            # 4. Route to next state (The State Machine)
            if result == condition.outcome:
                current_task_name = condition.target_task_success
                print(f"[Flow Manager] Match successful. Moving pointer to -> {current_task_name}")
            else:
                current_task_name = condition.target_task_failure
                print(f"[Flow Manager] Match failed. Moving pointer to -> {current_task_name}")

        print("--- Flow Execution Complete ---\n")

        return {
            "flow_id": self.config.id,
            "status": "completed",
            "execution_log": execution_log
        }
