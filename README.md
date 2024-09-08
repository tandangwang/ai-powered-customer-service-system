# AI-Powered Customer Service System

## Project Overview

This project implements an AI-powered customer service system that integrates conversational AI, retrieval-augmented generation (RAG), and persistent storage. It's designed to provide intelligent, context-aware responses to user queries while maintaining conversation history.

## Modules

### 1. Conversation Handler (langchain_module.py)

The core module that orchestrates the entire conversation flow.

Key features:
- Integrates MongoDB for conversation history storage
- Utilizes RAGFlow for retrieval-augmented generation
- Implements LangChain for language model interaction
- Manages user sessions and conversation context

Technologies used:
- LangChain
- Ollama (for language model)
- ChatPromptTemplate for structured prompts

### 2. RAGFlow Client (ragflow_module.py)

Handles interactions with the RAGFlow service for enhanced response generation.

Key features:

\- Creates and manages conversation sessions

\- Retrieves conversation history

\- Generates completions based on user input and context

\- Manages documents in the knowledge base

Technologies used:

- RESTful API interactions
- JSON data handling

**Knowledge Base Setup** 

Before using the RAGFlow Client, you need to create several knowledge bases within RAGFlow. The following test data sets are provided for this purpose, and all data is prepared in files located under the `test_data` directory:

\- `01_production_information`

\- `02_promotion_information`

\- `03_known_solutions`

\- `04_soft_skills`

You can categorize relevant information into these different knowledge bases as needed. Please note that all data is virtually created for testing purposes, so you may disregard any inconsistencies in the content.

**Key Additions:**

Mentioned that the data files are located in the test_data directory.

Maintained clarity and professionalism in the language.

Feel free to modify any part of it to better fit your project's needs!

### 3. MongoDB Manager (mongodb_module.py)

Manages persistent storage of conversation history.

Key features:
- Inserts new conversation records
- Retrieves user conversation history with customizable limits

Technologies used:
- PyMongo for MongoDB interactions
- Datetime handling for conversation timestamps

## System Flow

1. User input is received and processed by the Conversation Handler.
2. User information is extracted, and a new conversation is initialized if necessary.
3. The RAGFlow client is used to retrieve relevant information based on the user's query.
4. The Conversation Handler generates a response using the language model, incorporating RAG results and conversation history.
5. The response is stored in MongoDB for future reference.
6. The system continues this loop for ongoing conversations.

## Setup and Usage

To set up and run the AI-Powered Customer Service System, follow these steps:

1. **Clone the Repository**  
   Clone the repository to your local machine using the following command:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**  
   Change to the project directory:
   ```bash
   cd /path/to/this/repo
   ```

3. **Create a Virtual Environment**  
   Use Conda to create a virtual environment named `aics`:
   ```bash
   conda create -n aics python=3.10
   ```

4. **Activate the Virtual Environment**  
   Activate the newly created virtual environment:
   ```bash
   conda activate aics
   ```

5. **Install Dependencies**  
   Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Application**  
   Start the application by running the main module:
   ```bash
   python langchain_module.py
   ```

### Note

Make sure you have Conda installed on your system. If you encounter any issues, please refer to the documentation for the respective tools.

## Dependencies

- LangChain
- Ollama
- PyMongo
- Requests

## Future Improvements

- Implement more advanced RAG techniques
- Enhance error handling and logging
- Add support for multiple language models
- Implement user authentication and authorization

## Contributing

We welcome contributions to the AI-Powered Customer Service System! If you would like to contribute, please follow these guidelines:

1. **Fork the Repository**  
   Create a fork of the repository on GitHub.

2. **Clone Your Fork**  
   Clone your forked repository to your local machine:
   ```bash
   git clone <your-fork-url>
   ```

3. **Create a New Branch**  
   Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**  
   Implement your changes and ensure that your code adheres to the project's coding standards.

5. **Test Your Changes**  
   Run tests to ensure that your changes do not break any existing functionality.

6. **Commit Your Changes**  
   Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add a brief description of your changes"
   ```

7. **Push to Your Fork**  
   Push your changes to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**  
   Go to the original repository and create a pull request from your forked repository. Provide a clear description of your changes and why they should be merged.

### Code of Conduct
Please adhere to the [Code of Conduct](link-to-code-of-conduct) in all interactions within the project.

Thank you for your contributions!

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software, including for commercial purposes, under the terms of the license.

### MIT License
