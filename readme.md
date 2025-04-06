# Setting Up the Python Virtual Environment

This guide explains how to create a Python 3 virtual environment and install all required packages from a `requirements.txt` file.

## Prerequisites
- Python 3 installed on your system.
- `pip` (Python package manager) installed.

## Steps

1. **Navigate to Your Project Directory**  
    Open a terminal and navigate to the directory where your project is located:
    ```bash
    cd /path/to/your/project
    ```

2. **Create a Virtual Environment**  
    Run the following command to create a virtual environment named `env`:
    ```bash
    python3 -m venv AiVoiceToOrder
    ```

3. **Activate the Virtual Environment**  
    - On **Windows**:
      ```bash
      .\AiVoiceToOrder\Scripts\activate
      ```
    - On **macOS/Linux**:
      ```bash
      source AiVoiceToOrder/bin/activate
      ```

4. **Install Required Packages**  
    Use `pip` to install all dependencies listed in the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

5. **Verify Installation**  
    Ensure all packages are installed correctly by checking the installed packages:
    ```bash
    pip list
    ```

6. **Deactivate the Virtual Environment**  
    When you're done, deactivate the virtual environment:
    ```bash
    deactivate
    ```

## Notes
- Always activate the virtual environment before running your project scripts.
- If `requirements.txt` is missing, you can generate it using:
  ```bash
  pip freeze > requirements.txt
  ```
