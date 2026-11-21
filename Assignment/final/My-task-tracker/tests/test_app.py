import json

import pytest
from task_tracker import app
from task_tracker.app import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    load_tasks,
    save_tasks,
)


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


def test_delete_missing_task(tmp_path):
    with pytest.raises(ValueError, match="Task 99 was not found"):
        delete_task(99, tmp_path / "tasks.json")


def test_load_tasks_rejects_unexpected_top_level_structure(tmp_path):
    file_path = tmp_path / "tasks.json"
    file_path.write_text('{"task": []}', encoding="utf-8")

    with pytest.raises(ValueError, match="expected a list of tasks"):
        load_tasks(file_path)


def test_load_tasks_rejects_task_with_missing_required_fields(tmp_path):
    file_path = tmp_path / "tasks.json"
    file_path.write_text('[{"id": 1, "title": "Study Python"}]', encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields: completed"):
        load_tasks(file_path)


@pytest.mark.parametrize(
    "task",
    [
        {"id": "1", "title": "Study Python", "completed": False},
        {"id": 1, "title": 42, "completed": False},
        {"id": 1, "title": "Study Python", "completed": 0},
        {"id": True, "title": "Study Python", "completed": False},
    ],
)
def test_load_tasks_rejects_incorrect_field_types(tmp_path, task):
    file_path = tmp_path / "tasks.json"
    file_path.write_text(json.dumps([task]), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid field types"):
        load_tasks(file_path)


def test_save_tasks_writes_json_data(tmp_path):
    file_path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "title": "Study Python", "completed": False}]

    save_tasks(tasks, file_path)

    assert json.loads(file_path.read_text(encoding="utf-8")) == tasks


def test_save_tasks_preserves_original_if_replacement_fails(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    original_content = '[{"id": 1, "title": "Original", "completed": false}]'
    file_path.write_text(original_content, encoding="utf-8")

    def fail_replace(source, destination):
        raise OSError("replacement failed")

    monkeypatch.setattr(app.os, "replace", fail_replace)

    with pytest.raises(OSError, match="replacement failed"):
        save_tasks([{"id": 2, "title": "Updated", "completed": False}], file_path)

    assert file_path.read_text(encoding="utf-8") == original_content
    assert list(tmp_path.iterdir()) == [file_path]
