"""A small command-line task tracker with JSON file storage."""
import argparse
import json
from pathlib import Path


DEFAULT_FILE = Path("tasks.json")


def load_tasks(file_path=DEFAULT_FILE):
    path = Path(file_path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks, file_path=DEFAULT_FILE):
    path = Path(file_path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


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


def complete_task(task_id, file_path=DEFAULT_FILE):
    tasks = load_tasks(file_path)
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks, file_path)
            return task
    raise ValueError(f"Task {task_id} was not found.")


def delete_task(task_id, file_path=DEFAULT_FILE):
    tasks = load_tasks(file_path)
    remaining = [task for task in tasks if task["id"] != task_id]
    if len(remaining) == len(tasks):
        raise ValueError(f"Task {task_id} was not found.")
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
