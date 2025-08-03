# 🤖 My Personal AI Assistant

My personal AI assistant: 
A local **Flet** web app powered by **Google Gemini** for intelligent conversations 
and direct **bash command execution**.  

It can answer and execute commands in succession until your task is completed.

---

## 🌟 Overview

This project is an **AI assistant designed for personal use**,  
transforming your local device into a **powerful hub** for AI-driven productivity and automation.

Built as a local web application with **Flet**,  
it provides a seamless chat interface to interact with a sophisticated AI,  
execute system commands, and manage the conversation history — all within your private environment.

### Disclaimer

I am not responsible for any code generated or executed by the AI (Google Gemini)
or provided by the user.  
Use the assistant at your own risk. 
Always review and validate any commands or scripts before running them. 

I disclaim any liability for unintended consequences resulting from execution.

---

## ✨ Key Features

### ✅ Current Capabilities

- **Local Flet Web App Interface**  
  Access your AI assistant through a modern, 
  intuitive chat interface hosted locally on your machine.

- **Google Gemini Integration**  
  Leverage the power of Google's Gemini Pro model for intelligent 
  and context-aware conversations.

- **Direct Bash Command Execution (:)**  
  Execute shell commands directly from the chat, 
  enabling powerful system automation and fast task execution.

- **Recursive Iterations (-r or -:r)**
  
  The Bot can chat with itself using its output as his next prompt in order to complete
  your task step by step. 

  It can also execute a bash command, read its output and continue with other commands
  until your task is completed.

- **File-Based Chat History**  
  Your conversation history is automatically saved to a local `.txt` file.

---

### 🚧 Upcoming Enhancements (Roadmap)

- **Improved UI**
  Improve the quality and readability of the frontend part.


- **"Memory" via File Processing**  
  Expand the AI's knowledge base by feeding it documents, PDFs, code, and more.

- **Multi-AI Interactions**  
  Chat with multiple specialized AI agents 
  (e.g., "Linux Expert", "Creative Writer", "Financial Analyst").

- **Proactive Information Retrieval**  
  Program the assistant to fetch and present useful information like:
  - Global news or topic-specific updates  
  - Market and financial trends  
  - Local weather forecasts  
  - Personal agenda and reminders  

---

## 💡 Why a Local Flet App?

Choosing Flet for local deployment brings several advantages:

- **Ultimate Privacy & Control**  
  Your data and commands stay entirely on your local machine.

- **No Hosting Costs**  
  Run your AI assistant without external servers or subscriptions.

- **Seamless Integration**  
  Interacts directly with your local file system and shell for deeper automation.

- **Portability via Mobile (Optional)**  
  While built for desktop, core components could be used via Termux on mobile devices.

---

## 🚀 Getting Started

To launch your personal AI assistant:

### 1. Clone this repository

```bash
git clone https://github.com/gobbez/Flet_Gemini_AI_assistant.git
cd Flet_Gemini_AI_assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Google Gemini API Key

Get your API key from Google AI Studio

Create a keys.py file with GEMINI_KEY


### 4. Run the application

```bash
python main_frontend.py
```

If you want to make the bot execute sudo commands you can run via sudo:

```bash
sudo python main_frontend.py
```

---

## ⚙️ Available commands

These are the current commands that you can use to engage with the AI Assistant.

- : 

  Start your message with : to execute a bash command 
  (e.g ":ls", ":mkdir folder", ":nmap ip")

- -r

  Start your message with -r to enable recursive chat. 
  The bot will enter a loop passing its output as a next input in order to answer 
  your task. It will automatically stop whenever it thinks the task is answered.
  (e.g "-rWrite numbers from 1 to 5. You can write one number per message")

- -:r

  Start your message with -:r to enable recursive commands. 
  The bot will enter a loop executing bash commands and using the command output as 
  input for his successive command(s). It will automatically stop whenever it thinks 
  the task is completed.
  NB: In this case you can even use general language to make it create and execute
  commands for you!
  (e.g "-:rStep1: check my ip. Step2: ping my ip. Execute one step per message")

- -f

  Start your message with -f for file creation.
  The bot will process and create a file with the format you asked 
  (for now only .py and .txt works, but you can add whatever file you want)

---

## ✍️ Contributing

Anyone is free to contribute. 

This project embraces AI, Bash, Penetration Testing and modularity, so everyone can join!

---

## 📜 License
This project is open-source and available under the [MIT License](./LICENSE)

---

### 👨‍💻 About Me

Hi, I'm Andrea!
I'm a Python backend developer. 
Recently, I dove into the world of AI, Data Science and Penetration Testing.
I’m passionate about creating useful bots and experimenting with automation.

This project is a personal playground combining my curiosity for AI, Bash, and productivity tools, 
with a hint of Penetration Testing too!