# 📜 Historical Court Multi-Agent System (ADK)

## 🧠 Overview
This project is a Multi-Agent Historical Analysis System built using Google Agent Development Kit (ADK).  
The system simulates a historical court where multiple AI agents investigate historical figures or events and produce a balanced final report.

The project is designed to demonstrate multi-agent collaboration using tools and cloud-based AI services.

Source code is hosted on GitHub and designed for educational demonstration.

---

## 🎯 Project Objective
The objective of this project is to:

- Demonstrate multi-agent workflow design  
- Perform historical research from multiple perspectives  
- Automatically validate evidence balance  
- Generate neutral historical reports  

---

## 🏛️ System Concept
The system simulates a historical court process:

### 1️⃣ Investigation Phase
- Supporter Agent → Finds achievements and legacy  
- Critic Agent → Finds controversies and failures  

### 2️⃣ Trial Phase (Loop Validation)
- Judge Agent checks evidence balance  
- If data is insufficient → Investigation repeats  

### 3️⃣ Final Verdict Phase
- Generates neutral historical report  
- Saves report into file system  

---

## ⚙️ System Architecture

---

## 🤖 Agents Description

### 🟢 Admirer Agent
Responsible for researching:
- Achievements  
- Contributions  
- Positive legacy  

---

### 🔴 Critic Agent
Responsible for researching:
- Controversies  
- Criticism  
- Historical failures  

---

### ⚖️ Judge Agent
Responsible for:
- Checking balance between positive and negative data  
- Controlling loop exit condition  

---

### 📝 Verdict Writer Agent
Responsible for:
- Creating neutral historical analysis  
- Generating final report  
- Saving report into `/historical_reports`  

---

## 📦 Technologies Used
- Python 3.12  
- Google ADK  
- LangChain Community Tools  
- Wikipedia API  
- Google Cloud Logging  

---

## 📂 Project Structure

---

## 🚀 Installation

### 1️⃣ Clone Repository

---

### 2️⃣ Install Dependencies

---

### 3️⃣ Setup Environment Variables
Create `.env` file


---

## ▶️ Run Project

---

## 💬 Example Usage

User Input Example:

System Output:
- Positive historical evidence  
- Negative historical evidence  
- Balanced historical analysis report  

---

## 📊 Output
Generated reports will be saved inside:


Example Output:

---

## 🧪 Key Features
- Multi-Agent Collaboration  
- Parallel Historical Research  
- Loop-Based Evidence Validation  
- Automatic Report Generation  
- Cloud Logging Integration  

---

## 📚 Learning Outcomes
This project demonstrates:

- Multi-agent workflow architecture  
- Loop control in agent systems  
- Tool-based knowledge retrieval  
- State-based data sharing between agents  

---

## ⚠️ Disclaimer
This system is designed for educational purposes.  
Historical data is retrieved from public knowledge sources and may require verification.

---

## 👨‍💻 Author
Student Project — Industrial Physics and IoT Engineering  

---

## 📄 License
Educational Use Only

