import pytest
from task_tracker.app import add_task, list_tasks, complete_task, delete_task


def test_add_and_list_task(tmp_path):
    file_path = tmp_path / "tasks.json"
    task = add_task("Study Python", file_path)
    assert task["id"] == 1
    assert list_tasks(file_path) == [task]


def test_reject_empty_task_title(tmp_path):
    with pytest.raises(ValueError):
        add_task("   ", tmp_path / "tasks.json")


def test_complete_task(tmp_path):
    file_path = tmp_path / "tasks.json"
    add_task("Finish assignment", file_path)
    completed = complete_task(1, file_path)
    assert completed["completed"] is True


def test_delete_task(tmp_path):
    file_path = tmp_path / "tasks.json"
    add_task("Temporary task", file_path)
    delete_task(1, file_path)
    assert list_tasks(file_path) == []


def test_complete_missing_task(tmp_path):
    with pytest.raises(ValueError, match="was not found"):
        complete_task(99, tmp_path / "tasks.json")
