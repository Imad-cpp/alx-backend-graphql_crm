"""
# Celery Setup Guide

This guide explains how to set up and run the Celery worker and scheduler for the CRM application.

## Setup Steps

1.  **Install Redis and Dependencies**:
    Install Redis on your system (e.g., `sudo apt install redis-server`).
    Install the Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Migrations**:
    The `django-celery-beat` library requires database tables for storing schedules. Run this command from your project root.
    ```bash
    python manage.py migrate
    ```

3.  **Start Celery Worker**:
    Open a terminal, navigate to the project root, activate your virtual environment, and run:
    ```bash
    celery -A crm worker -l info
    ```

4.  **Start Celery Beat (Scheduler)**:
    Open a **second** terminal, navigate to the project root, activate your virtual environment, and run:
    ```bash
    celery -A crm beat -l info
    ```

5.  **Verify Logs**:
    To see the output of the scheduled report task, monitor the log file:
    ```bash
    tail -f /tmp/crm_report_log.txt
    ```
"""
