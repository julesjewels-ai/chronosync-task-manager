# ChronoSync Task Manager

A productivity application that dynamically schedules tasks based on the user's individual circadian rhythm and real-time energy levels rather than arbitrary time slots. By analyzing sleep data from wearables and manual energy logs, the system identifies the user's 'biological peak' hours. It then automatically reshuffles the daily agenda to allocate high-cognitive 'deep work' during peak alertness and administrative 'shallow work' during energy dips, maximizing efficiency and reducing burnout.

## Tech Stack

- React Native
- Node.js
- PostgreSQL
- TensorFlow.js
- Apple HealthKit
- Google Fit API

## Features

- AI-driven Chronotype Assessment
- Dynamic Calendar Rescheduling
- Biometric Energy Level Integration
- Task Complexity Categorization
- Burnout Prevention Alerts

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd chronosync-task-manager
make install

# Run the application
make run
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
make install && make run
```

## Development

```bash
make install  # Create venv and install dependencies
make run      # Run the application
make test     # Run tests
make clean    # Remove cache files
```

## Testing

```bash
pytest tests/ -v
```
