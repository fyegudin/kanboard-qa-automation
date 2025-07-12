from faker import Faker
import time
import allure
from functools import wraps  # Important for preserving function metadata

fake = Faker()

def generate_project_name():
    return f"Project {fake.name()} {fake.random_number(digits=3)}"

def generate_task_title():
    return f"Task {fake.text(max_nb_chars=5)} {fake.random_number(digits=2)}"

def generate_description():
    return f"Description: {fake.text(max_nb_chars=30)}"


def measure_execution_time(step_name: str = "Function Execution Time", time_expected: float | None = None):
    """
    A decorator to measure the execution time of a function
    and report it as an Allure step.

    Args:
        step_name (str): The name for the Allure step.
        :param step_name:
        :param time_expected:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with allure.step(step_name):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                elapsed_time = end_time - start_time

                # Attach the elapsed time to the Allure report
                allure.attach(
                    f"Execution Time: {elapsed_time:.4f} seconds",
                    name="Performance Metric",
                    attachment_type=allure.attachment_type.TEXT
                )
                if time_expected:
                    assert elapsed_time < time_expected, (f"Expected execution time - {time_expected} seconds,"
                                                          f" but got {elapsed_time:.4f} seconds")
                return result

        return wrapper

    return decorator