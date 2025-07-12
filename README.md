# Kanboard QA Automation Framework (with Poetry)

This repository contains automated tests for Kanboard project management application using Poetry for dependency management.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.12
- Poetry (installation: `pip install poetry`)

### Installation
1. Clone this repository
2. Start the Kanboard environment:
   ```bash
   docker-compose up -d

### Commands:

#### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/kanboard-qa-automation.git
   cd kanboard-qa-automation
2. Start the Kanboard environment:
   ```bash
   docker-compose up -d
3. Install dependencies with Poetry:
   ```bash
   poetry install
4. Install Playwright browsers:
   ```bash
   poetry run playwright install

#### Running Tests Using Poetry commands:

1. Run all tests:
   ```bash
   poetry run tests
2. Run with Allure reporting:
   ```bash
   poetry run tests-with-report
3. Run specific test suite:
   ```bash
   poetry run pytest tests/test_project_creation.py -v
   
#### Running Tests Using Pytest commands:

1. Run all tests:
   ```bash
    pytest -v
2. Run with Allure reporting:
   ```bash
   pytest -v --alluredir=./allure-results ; allure serve ./allure-results

#### Alternative: Activate virtualenv first:

1. Poetry command is designed to activate your project's virtual environment :
   ```bash
   poetry shell
2. Allure Directory for reporting:
   ```bash
   pytest --alluredir=./allure-results
3. Generate allure report:
   ```bash
    allure serve ./allure-results
4. To leave the virtualenv:
   ```bash
    exit

## Test Plan

### 1. Project Creation Validation
**Objective**: Verify projects created via UI are correctly stored in the database  
**Steps**:
1. Create new project through Kanboard UI
2. Verify project appears in `projects` table
3. Validate required fields:
   - Name matches input
   - `is_active` = true
   - `is_public` = false
   - `last_modified` ≠ null

**Validation**: Database query + UI assertion  
**Success**: Database records match UI input with correct field values

### 2. Task Lifecycle Testing
**Objective**: Validate task status changes propagate to database  
**Steps**:
1. Create task in project via UI
2. Verify task in `tasks` table with `status=1` (open)
3. Move task to "Done" column in UI
4. Verify task `status=2` (closed) in database

**Validation**: Database state before/after UI operations  
**Success**: Database status matches UI column position

### 3. Data Integrity Check
**Objective**: Verify project deletion cascades to tasks  
**Steps**:
1. Create project with multiple tasks via UI
2. Delete project via UI
3. Verify:
   - Project removed from `projects` table
   - All tasks removed from `tasks` table
   - No orphaned tasks remain

**Validation**: Database queries before/after deletion  
**Success**: No residual records for deleted project/tasks

### 4. Basic Performance Test
**Objective**: Measure system performance under load  
**Steps**:
1. Create new project
2. Create 50 tasks via UI
3. Measure:
   - Database retrieval time for all tasks
   - Project board load time
4. Verify:
   - Database query <1 second
   - UI remains responsive

**Validation**: Timing measurements  
**Success**: All operations complete within thresholds
