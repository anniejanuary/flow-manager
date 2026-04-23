# Flow Manager Microservice

## Overview
The Flow Manager is a lightweight, dynamic orchestration microservice built with FastAPI. It operates as a state machine, executing tasks sequentially based on a completely decoupled JSON configuration. This architecture separates the **configuration** (the map) from the **execution** (the code), allowing for highly flexible, dynamic workflows without hardcoding logic.

---

## Flow Design & Architecture

### 1. How do the tasks depend on one another?
Tasks in this system do not have hardcoded dependencies in the Python codebase: 
* The actual Python functions (the tasks) are completely isolated and independent from one another.
* Their execution order is dictated strictly by the `conditions` array in the JSON payload. 
* The JSON acts as a routing table (or a map). The engine acts as a pointer, reading the JSON to determine which registered Python function to execute next. This means you can reorder, skip, or create loops between tasks simply by modifying the JSON configuration, without touching a single line of backend code.

### 2. How is the success or failure of a task evaluated?
Task evaluation is based on standardized string return values:
* Each registered task function is designed to return a specific state string (e.g., `"success"`, `"failure"`, `"skipped"`).
* If a task crashes or throws a Python exception, the engine gracefully catches the error and automatically assigns it a status of `"error"`.
* After the task completes, the `FlowEngine` captures this result and looks up the corresponding `condition` block for that specific `source_task` in the JSON. It then compares the task's actual return value to the expected `outcome` defined in that condition.

### 3. What happens if a task fails or succeeds?
The flow engine routes to the next state based on the match between the task's result and the condition's expected outcome:
* **Match (Success Path):** If the actual result matches the condition's `outcome` (e.g., both are `"success"`), the engine dynamically updates its current pointer to the task defined in `target_task_success`.
* **Mismatch (Failure/Alternate Path):** If the result does NOT match the expected outcome (or if an exception occurred resulting in `"error"`), the engine updates its pointer to the task defined in `target_task_failure`.
* **Termination:** If the target task is explicitly defined as `"end"`, or if a task has no corresponding conditions defined in the JSON, the execution loop breaks. The flow terminates cleanly and returns a comprehensive execution log to the API caller.

---

## Quick Start & Testing Guide

### 1. Running the Server
Before testing, ensure your virtual environment is active and dependencies are installed (`pip install fastapi uvicorn`).

From the root project directory, run:
```bash
uvicorn main:app --reload
```

The server will start at http://127.0.0.1:8000.

### 2. Testing via Swagger UI (Interactive Docs)
FastAPI provides a built-in interface to test your endpoints without external tools.

Open your browser and navigate to: http://127.0.0.1:8000/docs

Locate the POST endpoint: /api/v1/flow/execute.

Click the "Try it out" button.

Paste the Example Payload below into the Request Body.

Click Execute.

### 3. Example Payload
Use this JSON to test the sequential execution of Task 1 → Task 2 → Task 3:

```json
{
  "flow": {
    "id": "flow123",
    "name": "Data processing flow",
    "start_task": "task1",
    "tasks": [
      {"name": "task1", "description": "Fetch data"},
      {"name": "task2", "description": "Process data"},
      {"name": "task3", "description": "Store data"}
    ],
    "conditions": [
      {
        "name": "condition_task1_result",
        "description": "Evaluate the result of task1. If successful, proceed to task2; otherwise, end the flow.",
        "source_task": "task1",
        "outcome": "success",
        "target_task_success": "task2",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task2_result",
        "description": "Evaluate the result of task2. If successful, proceed to task3; otherwise, end the flow.",
        "source_task": "task2",
        "outcome": "success",
        "target_task_success": "task3",
        "target_task_failure": "end"
      }
    ]
  }
}
```

### 4. Expected Result
The server response will include an execution_log showing each task that ran and its status. If you have registered the POC tasks, you will see the simulated logs in your terminal as well.
```json
{
  "flow_id": "flow123",
  "status": "completed",
  "execution_log": [
    { "task": "task1", "status": "success" },
    { "task": "task2", "status": "success" },
    { "task": "task3", "status": "success" }
  ]
}
```

### 5. Logging
All task executions and their outcomes are logged to the console for easy debugging and monitoring. You can see the logs in the terminal where you started the server. Each log entry includes the task name and its result (e.g., "success", "failure", "error"). This allows you to trace the flow execution in real-time and identify any issues quickly.