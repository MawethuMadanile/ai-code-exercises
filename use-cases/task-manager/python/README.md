# TaskManager

A lightweight command-line task management tool for tracking tasks, priorities, and deadlines from your terminal.

## Features

- Create tasks with titles, descriptions, priorities, and due dates
- Update task status through a defined workflow (todo → in progress → review → done)
- Filter and list tasks by status, priority, or overdue state
- Tag tasks for flexible organisation
- Persistent JSON storage — tasks survive between sessions
- Task statistics and completion tracking

## Technologies

Python 3.8+, standard library only (argparse, json, uuid, datetime)

## Installation

Clone the repository and navigate into the project folder:

```bash
git clone https://github.com/wethinkcode/ai-code-exercises.git
cd ai-code-exercises/use-cases/task-manager/python
```

No external dependencies — run straight away with Python 3.8 or higher.

## Usage

```bash
# Create a task
python cli.py create "Fix login bug" -d "Null pointer on empty input" -p 3 -u 2024-12-31 -t backend,urgent

# List all tasks
python cli.py list

# Filter by status
python cli.py list -s in_progress

# Update status
python cli.py status <task_id> done

# Show overdue tasks
python cli.py list -o

# Add or remove a tag
python cli.py tag <task_id> frontend
python cli.py untag <task_id> frontend

# View statistics
python cli.py stats
```

## Configuration

By default tasks are saved to `tasks.json` in the working directory. To use a different file, modify the `storage_path` argument when instantiating `TaskManager` in `cli.py`.

## Project Structure