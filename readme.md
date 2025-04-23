# About this Project

This project is an AI-powered voice assistant designed to streamline the process of taking customer orders for a restaurant. It leverages advanced AI technologies to provide a conversational interface for customers, allowing them to place and customize their orders seamlessly.

## Key Features

- **Agent with Tool Calling**: Utilizes AI agents capable of calling tools to create, update, and delete customer orders.
- **LangGraph and LangChain Integration**: Leverages LangGraph and LangChain frameworks to build and manage conversational AI workflows, enabling seamless integration of language models and tools.
- **Speech Recognition**: Captures and transcribes customer speech for processing.
- **Text-to-Speech**: Converts AI responses into audio to communicate with customers.
- **Order Management**: Handles adding, updating, and finalizing customer orders.
- **Menu Integration**: Provides a detailed menu and suggests add-ons to enhance the customer experience.
- **Multi-Processing**: Ensures smooth operation by handling simultaneous tasks like listening and responding in real-time.

This project is designed to improve efficiency and customer satisfaction by automating the order-taking process while maintaining a natural conversational flow.

# Setting Up the Python Virtual Environment

This guide explains how to create a Python 3 virtual environment and install all required packages from a `requirements.txt` file.

## Prerequisites

- Python 3 installed on your system.
- `pip` (Python package manager) installed.
- OpenAI api key

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

## Set Up Environment Variables

Create a `.env` file in the project directory and add the following line to specify your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

Ensure the `.env` file is included in your `.gitignore` file to prevent exposing sensitive information.

## Notes

- Always activate the virtual environment before running your project scripts.
- If `requirements.txt` is missing, you can generate it using:
  ```bash
  pip freeze > requirements.txt
  ```
