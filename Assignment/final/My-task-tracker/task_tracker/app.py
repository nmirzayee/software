"""A small command-line task tracker with JSON file storage."""
import argparse
import json
import os
from pathlib import Path
import tempfile


DEFAULT_FILE = Path("tasks.json")


def load_tasks(file_path=DEFAULT_FILE):
    path = Path(file_path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        tasks = json.load(file)

    if not isinstance(tasks, list):
        raise ValueError("Invalid task data: expected a list of tasks.")

    required_fields = {"id", "title", "completed"}
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise ValueError(
                f"Invalid task data: task at index {index} must be an object."
            )
        missing_fields = required_fields - task.keys()
        if missing_fields:
            fields = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Invalid task data: task at index {index} is missing "
                f"required fields: {fields}."
            )
        if (
            type(task["id"]) is not int
            or not isinstance(task["title"], str)
            or not isinstance(task["completed"], bool)
        ):
            raise ValueError(
                f"Invalid task data: task at index {index} has invalid field "
                "types; expected integer id, string title, and boolean completed."
            )

    return tasks


def save_tasks(tasks, file_path=DEFAULT_FILE):
    path = Path(file_path)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            json.dump(tasks, file, indent=2)
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def add_task(title, file_path=DEFAULT_FILE):
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    tasks = load_tasks(file_path)
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    save_tasks(tasks, file_path)
    return task


def list_tasks(file_path=DEFAULT_FILE):
    return load_tasks(file_path)


def _find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task {task_id} was not found.")


def complete_task(task_id, file_path=DEFAULT_FILE):
    tasks = load_tasks(file_path)
    task = _find_task(tasks, task_id)
    task["completed"] = True
    save_tasks(tasks, file_path)
    return task


def delete_task(task_id, file_path=DEFAULT_FILE):
    tasks = load_tasks(file_path)
    _find_task(tasks, task_id)
    remaining = [task for task in tasks if task["id"] != task_id]
    save_tasks(remaining, file_path)


def main():
    parser = argparse.ArgumentParser(description="A simple task tracker.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("title")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as completed")
    done_parser.add_argument("id", type=int)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()
    try:
        if args.command == "add":
            task = add_task(args.title)
            print(f"Added task {task['id']}: {task['title']}")
        elif args.command == "list":
            tasks = list_tasks()
            if not tasks:
                print("No tasks yet.")
            for task in tasks:
                status = "✓" if task["completed"] else " "
                print(f"[{status}] {task['id']}: {task['title']}")
        elif args.command == "done":
            complete_task(args.id)
            print(f"Task {args.id} completed.")
        elif args.command == "delete":
            delete_task(args.id)
            print(f"Task {args.id} deleted.")
    except (ValueError, json.JSONDecodeError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
