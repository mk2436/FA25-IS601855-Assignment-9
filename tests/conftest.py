# tests/conftest.py

import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright
import requests
import logging
from test_logging_config import setup_test_logging, setup_integration_test_logging, setup_e2e_test_logging


@pytest.fixture(scope="session", autouse=True)
def setup_logging_for_tests():
    """
    Set up logging for all tests based on the test type.
    """
    # Determine test type based on the test file path
    import os
    test_file = os.environ.get('PYTEST_CURRENT_TEST', '')
    
    if 'e2e' in test_file:
        logger = setup_e2e_test_logging()
    elif 'integration' in test_file:
        logger = setup_integration_test_logging()
    else:
        logger = setup_test_logging()
    
    logger.info("Test logging configured")
    return logger


@pytest.fixture(scope='session')
def fastapi_server():
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    logger = logging.getLogger(__name__)
    
    # Start FastAPI app
    logger.info("Starting FastAPI server for E2E tests...")
    fastapi_process = subprocess.Popen(['python', 'main.py'])
    
    # Define the URL to check if the server is up
    server_url = 'http://127.0.0.1:8000/'
    
    # Wait for the server to start by polling the root endpoint
    timeout = 30  # seconds
    start_time = time.time()
    server_up = False
    
    logger.info("Waiting for FastAPI server to start...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                logger.info("FastAPI server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    if not server_up:
        fastapi_process.terminate()
        logger.error("FastAPI server failed to start within timeout period.")
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    # Terminate FastAPI server
    logger.info("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait()
    logger.info("FastAPI server has been terminated.")


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """
    Fixture to manage Playwright's lifecycle.
    """
    logger = logging.getLogger(__name__)
    logger.info("Initializing Playwright...")
    
    with sync_playwright() as p:
        yield p
    
    logger.info("Playwright instance closed.")


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """
    Fixture to launch a browser instance.
    """
    logger = logging.getLogger(__name__)
    logger.info("Launching browser for E2E tests...")
    
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    
    logger.info("Closing browser...")
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """
    Fixture to create a new page for each test.
    """
    logger = logging.getLogger(__name__)
    logger.debug("Creating new browser page...")
    
    page = browser.new_page()
    yield page
    
    logger.debug("Closing browser page...")
    page.close()
