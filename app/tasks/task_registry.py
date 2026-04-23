from typing import Callable


class TaskRegistry:
    """
    A dynamic registry that maps string names from the JSON
    to actual Python functions anywhere in your codebase.
    """
    _tasks: dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, func: Callable) -> None:
        """
        Registers a function under a string name.
        Args:
            name (str): The name to register the function under (should match the JSON).
            func (Callable): The actual function to execute when this task is called.
        """
        cls._tasks[name]: Callable = func

    @classmethod
    def get_task(cls, name: str) -> Callable:
        """
        Retrieves the function by name.
        Args:
            name (str): The name of the task to retrieve.
        Returns:
            Callable: The function associated with the given name.
        """
        if name not in cls._tasks:
            raise NotImplementedError(f"Task '{name}' has not been registered.")
        return cls._tasks[name]
