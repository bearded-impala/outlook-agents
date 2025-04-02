# 🧠 Multi-Agent Outlook Orchestration App

This repository provides a lightweight multi-agent orchestration system for Microsoft Outlook using local Ollama LLMs and CrewAI. It continuously monitors Outlook inboxes and processes emails with specialized agents for classification, summarization, urgency detection, tone analysis, and auto-reply generation.

## ✨ Features

- ✅ **CrewAI-powered orchestration** of independent agents
- 📥 **Multiple inbox support**
- 🧠 **Email categorization** into `Work`, `Personal`, `Urgent`, etc.
- ✍️ **Summary, tone, urgency detection**, and **response drafting**
- 📨 **Outlook draft auto-reply generation**
- ⚡ Uses **quantized LLMs (via Ollama)** for CPU-only inference
- 🔁 Runs continuously in the background with polling
- 🧩 Modular and easily customizable agent/task configuration
- 💻 Designed to be lightweight for laptop/desktop users — no GPU required
- 📤 The application uses COM automation (via pywin32) to interact with Outlook. Ensure Outlook is running and accessible.
- 🦙 Ollama must be running in the background. First-time setup may pull the model.

## 🧰 Prerequisites

- Windows with Microsoft Outlook installed and configured
- Python 3.10 or later
- Git + pip

## 🧪 How to Run

1. **Clone the repo and create a virtual environment**:

   ```bash
   git clone https://github.com/bearded-impala/outlook-agents.git && cd outlook-agents
   python -m venv outlook-agents && outlook-agents\Scripts\activate && python -m pip install --upgrade pip
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

3. ** Update `src/config/config.py` **
   Update IDENTITY as per your preference

4. **Run the application:**
   The app will run in the background and monitor your Outlook inbox.

   ```
   python src/main.py
   ```

5. **Build/Package (optional):**
   You can create a standalone executable using PyInstaller if needed.

   ```
   pip install pyinstaller
   pyinstaller --onefile --windowed --icon=src/app.ico src/main.py
   ```

6. **Configure the Application to Run Automatically (optional):**
   To run the app continuously in the background, set up a scheduled task using Windows Task Scheduler:

   - Open Task Scheduler: Press `Win + R`, type `taskschd.msc`, and press `Enter`.
   - Create a New Task: In the right-hand pane, click Create Task
   - General Tab: Name, Select Run whether user is logged on or not, Check Run with highest privileges if necessary
   - Triggers Tab: Click New...In the Begin the task dropdown, select At startup.
   - Actions Tab: Click New...For Action, select Start a program. In Program/script, browse to the generated executable in your dist folder (e.g., C:\path\to\multi_agent_outlook.exe). Set the Start in field to the executable's directory.

7. **Create a Windows Installer**
   - Download https://jrsoftware.org/isdl.php#stable
   - Open Inno Setup
   - Open your `installer.iss`
   - Click Compile
   - 👉 Result: `OutlookAgentsInstaller.exe` – a full installer with logo, shortcut, and Task Scheduler setup 🎉

## ⚙️ Configuration (`src/config/config.py`)

    IDENTITY: Your Persona
    MODEL_NAME: The model must be from https://ollama.com/search (e.g., gemma:2b, llama3, mistral, etc.)
    POLLING_INTERVAL: How frequently the app checks for new emails in seconds

## 🧩 Components and Their Purposes

This project leverages several libraries, models, and tools to create a lightweight, CPU-efficient multi-agent orchestration app for Microsoft Outlook. Below is an overview of everything used and its purpose:

- **pywin32**  
  _Purpose:_ Enables COM automation to interact with Microsoft Outlook. It allows the app to read emails, mark them as read, and access other Outlook functionalities.

- **crewai**  
  _Purpose:_ Serves as the multi-agent orchestration framework. Crew AI is used to register and manage the execution of our agents (Inbox Scanner, Summarizer, Urgency Detector, Tone Analyzer, Auto-Responder, Follow-up Tracker, and Task Manager).

- **BeautifulSoup (bs4)**  
  _Purpose:_ Cleans up and extracts readable text from email HTML content. Used to strip HTML tags and formatting artifacts while preserving readable structure.

- **PyInstaller**
  _Purpose:_ Packages the Python application into a standalone executable. This is useful for deployment on systems that do not have Python pre-installed.

- **Windows Task Scheduler**
  _Purpose:_ Configures the application to run automatically at system startup or on a defined schedule, ensuring continuous background operation.
