# **Robot: A Context-Aware Terminal Assistant**

## **1\. Abstract**

Robot is a command-line tool that enhances your terminal with an integrated, context-aware AI assistant. By activating a Robot session, the tool transparently records your commands and their outputs, building a complete context of your work. At any point, you can invoke robot with a natural language question to get intelligent insights, summaries, or explanations based on the activity in your current session. It's designed to feel like a native feature of your shell, providing the power of a large language model without interrupting your workflow.

## **2\. The Vision**

The goal of Robot is to seamlessly integrate an intelligent assistant into the command-line environment. The terminal is a developer's most powerful tool, but recalling specific commands, deciphering complex outputs, and keeping track of a multi-step process can be challenging.

Robot addresses this by creating an "enhanced" terminal session that maintains a memory of your actions. This session history serves as a dynamic context for an LLM, allowing you to ask complex questions that relate to previous commands and their results. This moves beyond simple command-lookup and toward a genuine conversational partner for your development tasks.

## **3\. How It Works**

The interaction model is designed to be unobtrusive, similar to activating a Python virtual environment.

### **Core Workflow**

1. **Activate a Session:** You begin by starting a Robot-aware session. This command launches a new sub-shell where all input and output will be monitored.

```bash
robot activate
```

Your terminal prompt will change slightly to indicate that you are in an active Robot session.
2. **Work as Usual:** Use the terminal as you normally would. Robot works in the background, logging your commands and their results.

```bash
(robot) $ ls -l
total 8
-rw-r--r--  1 user  staff  1024 Jul 11 10:30 data.csv
-rwxr-xr--  1 user  staff  2560 Jul 11 10:32 process.sh

(robot) $ head -n 2 data.csv
id,value,timestamp
1,42,2025-07-11T10:30:00Z
```

3. **Ask a Question:** When you need help or information, use the robot command followed by your question in plain English.

```bash
(robot) $ robot "Based on the files here, what is the purpose of the shell script?"
```

4. **Get an Answer:** Robot analyzes the recorded session context (the ls and head commands and their output) and provides a relevant answer.

```bash
> The script 'process.sh' likely processes the 'data.csv' file. The CSV file contains columns named 'id', 'value', and 'timestamp'.
```

5. **Deactivate the Session:** When you're done, you can exit the session and return to your normal shell.

```bash
(robot) $ exit
$
```

## **4\. Technical Plan**

This project will be developed in Python, focusing on robust session management and seamless LLM integration.

### **Core Components:**

1. **Session Management (Pseudo-Terminal):**
   * The core of Robot's functionality will rely on Python's pty module. The `robot activate` command will spawn a new user shell (e.g., /bin/bash or /bin/zsh) as a child process running within a pseudo-terminal.
   * The main Robot process will act as the master of the pty, allowing it to read all output from the shell (stdout) and write all input to it (stdin).  
2. **Background Logging:**  
   * During an active session, all I/O passing through the pseudo-terminal will be captured and written to a temporary log file.  
   * This log will be a structured record of the entire terminal session, preserving the sequence of commands and their exact outputs, which is crucial for providing accurate context to the LLM.  
3. **Command-Line Interface (CLI):**  
   * We will use **Typer** to build the CLI.  
   * The primary commands will be:
     * `robot activate`: Starts the monitored session.
     * `robot deactivate`: Ends the current session.
     * `robot <query>`: The command used within an active session to ask a question. This command will locate the session log, package it with the query, and send it to the LLM.
4. **LLM Integration:**  
   * The robot \<query\> command will read the entire content of the current session's log file.  
   * This content will be formatted into a prompt for a large language model. The prompt will be engineered to instruct the LLM to act as a terminal assistant and answer the user's query based on the provided session transcript.  
   * The response from the LLM will be printed directly to the terminal.

## **5\. Project Roadmap**

The project will be developed in distinct phases, starting with the most critical functionality.

1. **Phase 1: Core Session Management**
   * \[x] Implement the `robot activate` command to successfully launch a sub-shell within a pseudo-terminal using Python's pty module.
    * \[x] Develop the background logging mechanism to capture all session I/O to a temporary file.
    * \[x] Create the basic `robot <query>` command that reads the log file and the user's query.
   * \[ \] Integrate with a foundational LLM API to establish the proof-of-concept pipeline.  
2. **Phase 2: Refinement and Usability**  
   * \[ \] Improve the prompt engineering to handle long session contexts and provide more accurate answers.  
   * \[ \] Implement clean session start-up and tear-down, including handling of the session log files.  
   * \[ \] Add configuration options (e.g., choosing the LLM provider, setting API keys).  
   * \[ \] Refine the in-session prompt to provide clear feedback to the user.  
3. **Phase 3: Advanced Features**  
   * \[ \] Explore options for session history, allowing users to ask questions about previous sessions.  
   * \[ \] Investigate using more efficient or local LLMs to improve privacy and reduce latency.  
   * \[ \] Add "intent detection" to suggest commands or actions, making Robot a more proactive assistant.  
4. **Phase 4: Distribution and Community**  
   * \[ \] Package the application for easy installation via PyPI.  
   * \[ \] Write comprehensive user and developer documentation.  
   * \[ \] Perform testing across different shells (bash, zsh, fish) and operating systems (Linux, macOS).

## Development Setup

Install in editable mode with dev dependencies:

```bash
pip install -e .[dev]
```

Run the command-line interface:

```bash
robot --help
```
