# StarrySpark---TalkToMao
TalkToMao — a dialogue system about revolutionary heroes based on AIGC. The project uses RAG retrieval-augmented generation technology, combined with the locally deployed ChatGLM3-6B large model, allowing users to have smart, time-crossing conversations with Comrade Mao Zedong, using technology to carry forward revolutionary culture.

## 📖 Project Overview

**TalkToMao** — A red revolutionary hero dialogue system based on AIGC. The project uses RAG (Retrieval-Augmented Generation) technology combined with a locally deployed ChatGLM3-6B large model, allowing users to have intelligent conversations with Comrade Mao Zedong across time and space, using technology to pass on red culture.

The project aims to address the pain points of traditional red education, such as "low interactivity and lack of appeal for young people," transforming red history into interactive and experiential dialogue scenes, bringing red culture out of books and into warm, engaging conversations.

**Core Concept**: Red culture as the soul, technology as the tool.

## ✨ Features

- **Intelligent Dialogue**: Answers questions in the first-person voice of Comrade Mao Zedong, with a calm and friendly tone
- **RAG-Enhanced Retrieval**: Based on authoritative historical sources like *Chronology of Mao Zedong* and *Biography of Mao Zedong*, ensuring answers are supported by facts
- **Multi-Round Dialogue Memory**: Maintains context for coherent conversations, achieving real "dialogue" rather than simple Q&A
- **Speech Synthesis**: Integrates Edge TTS to let "Comrade Mao Zedong" speak aloud
- **Multi-Platform Support**: Responsive web design, accessible on both desktop and mobile
- **Local Deployment**: All models and data run locally, no internet required, ensuring data security

## 🏗️ Technical Architecture

User (browser)
↓
Flask Web backend
↓
RAG retrieval (LangChain  ChromaDB)
↓
Local large model (ChatGLM3-6B  Ollama)
↑
Red knowledge base ("Chronicle of Mao Zedong", "Biography of Mao Zedong", etc.)


| Layer | Technology Choice | Description |
|-------|-----------------|------------|
| Large Model | ChatGLM3-6B | Domestic open-source, strong Chinese capability, local deployment |
| Deployment Tool | Ollama | One-click local deployment, no internet needed |
| RAG Framework | LangChain | Connects large model with knowledge base |
| Vector Database | ChromaDB | Lightweight, semantic search |
| Backend | Python Flask | Provides API interface |
| Frontend | HTML CSS JavaScript | Responsive UI, works on PC and mobile |
| Speech Synthesis | Edge TTS | Microsoft neural network voice |

## 🚀 Quick Start

### Environment Requirements

- Python 3.11 or higher
- At least 8GB of RAM
- At least 20GB of available disk space
- Windows / macOS / Linux

### Installation Steps

#### 1. Clone the Project

```bash
git clone https://github.com/ZenJoyfulMemories/StarrySpark---TalkToMao.git
```
#### 2. Create and activate a virtual environment
Windows:

```bash
python -m venv rag_env
rag_env\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv rag_env
source rag_env/bin/activate
```
#### 3. Install dependencies
```bash
pip install -r requirements.txt
```
#### 4. Install Ollama and download the model
Go to the Ollama official website to download and install it, then pull the model:

```bash
ollama pull chatglm3:6b-128k
```
#### 5. Prepare Historical Documents
Put your red historical documents (.docx or .txt) into the data/ folder.
It currently already includes the 'Chronology of Mao Zedong'.
#### 6. Build the Vector Database
```bash
python build_vector_store.py
```

#### 7. Start the App
Windows:

Double-click start.bat

macOS / Linux:

```bash
python app.py
```

#### 8. Access the App
Open http://localhost:5000 in your browser


### 🛠️ Configuration Instructions
##### Voice Switching
Modify the voice parameter in the /synthesize route of app.py:

```python
communicate = edge_tts.Communicate(text, "zh-CN-YunyangNeural")
```
##### Optional voices:

zh-CN-YunyangNeural — Calm and dignified (recommended)

zh-CN-YunjianNeural — Passionate and powerful

zh-CN-YunxiNeural — Sunny and energetic

##### Model Switching
To switch to a different large model, modify the following in app.py:

```python
llm = Ollama(
model="Your model name",
temperature=0.3,
top_p=0.9,
)
```

### 📝 Notes
First launch: The model loading takes some time, please be patient

Memory requirements: ChatGLM3-6B needs about 6GB of memory

Port usage: If port 5000 is occupied, you can change the port in app.py

Voice synthesis: Internet access to Microsoft TTS service is required

### 🤝 Contribution
Feel free to submit Issues and Pull Requests!

### 📄 License
MIT License

### 🙏 Thanks
ChatGLM — Open-source large language model

Ollama — Local model deployment tool

LangChain — RAG framework

Chroma — Vector database

## Honoring history with technology, passing on the red legacy through code.
