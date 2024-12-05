
# FOMO Radio Framework 🎙️

Welcome to the **FOMO Radio Framework**, an open-source solution to build AI-powered autonomous radio stations tailored for your use cases. Whether it's creating a dynamic crypto news station like **FOMO Radio** with RJ Diana or adapting it for sports commentary, market trends, or personalized summaries, this framework has you covered.

---

## 🌟 Features

1. **AI-Powered Content Aggregation**  
   Aggregate and analyze content from diverse sources with seamless integration.

2. **Dynamic Memory Management**  
   Powered by the `mem0` library, it maintains a dynamic memory system, enabling accurate recall of the latest and most relevant content.

3. **Automatic Summarization**  
   Structures and summarizes data automatically, preparing it for user engagement.

4. **Multimedia Output**  
   Generates audio and video summaries, ready for distribution across platforms.

5. **Export Capabilities**  
   Distributes summaries and multimedia files to social media, streaming services, or custom destinations.

---

## 💡 Use Cases

- 🎙️ **AI-Powered Radio Stations**  
   Create fully autonomous, topic-specific radio stations pulling real-time data.
   
- 🏟️ **Live Sports Commentary**  
   Deliver AI-driven play-by-play sports commentary, analyzing data from live feeds.

- 📰 **Unbiased News Production**  
   Pull verified content from multiple sources to create an autonomous, unbiased news channel.

- 🧑‍💻 **Personalized AI Companions**  
   Summarize news, social media trends, or market insights on-demand with unmatched clarity.

---

## 🛠️ Customization Options

### Current Framework Components
The FOMO Radio Framework currently integrates the following technologies:

1. **Data Collection**:  
   Twitter v2 APIs are used to fetch data for aggregation and analysis.

2. **AI Models**:  
   OpenAI's GPT models are used for natural language processing and summarization.

3. **Voice Generation**:  
   ElevenLabs is used to generate high-quality, natural-sounding voice outputs.

### How to Use Alternative Services
The FOMO Radio Framework is designed to be flexible, allowing you to use alternative data collection sources, AI models, or voice generation tools. To make these changes, you’ll need to modify specific files or add new implementations in the framework as outlined below:

---

### 1. Data Collection
If you'd like to fetch data from a source other than Twitter API v2, you need to:
- **Add a new data collector**:  
  Add your custom logic in the `data_collectors` folder by creating a new Python file. For example:
  - Create `data_collectors/custom_data_collector.py` to implement fetching logic for your desired source.
- **Update `run.py`**:  
  Import your custom data collector module and replace or integrate it with the existing data fetching process.

#### Example:
```python
from data_collectors.custom_data_collector import CustomDataCollector

data_collector = CustomDataCollector()
data = data_collector.fetch_data()
```

---

### 2. Audio Script Generation
To use an AI model other than OpenAI for generating audio scripts:
- **Add or modify a client in the `script_generators` folder**:  
  For example, create `script_generators/custom_llm_client.py` to implement your desired large language model (LLM).
- **Update `script_generators/llm_client.py`**:  
  Modify or replace the integration to use your custom LLM.
- **Update `run.py`**:  
  Import and use your custom LLM client.

#### Example:
```python
from script_generators.custom_llm_client import CustomLLMClient

llm_client = CustomLLMClient()
script = llm_client.generate_script(data)
```

---

### 3. Voice Generation
If you'd like to use a different voice generation tool (e.g., Amazon Polly, Google Text-to-Speech):
- **Modify `tts_transformers/base.py`**:  
  Add a custom class to interface with your preferred TTS (text-to-speech) service. Implement methods for generating and processing audio.
- **Update `run.py`**:  
  Import your new TTS transformer and replace or integrate it with the existing voice generation process.

#### Example:
```python
from tts_transformers.custom_tts import CustomTTS

tts = CustomTTS()
audio = tts.generate_voice(script)
```

---

### Summary of Changes
- **Data Collection**: Add your custom logic in the `data_collectors` folder and integrate it in `run.py`.
- **Audio Script Generation**: Create or modify a client in `script_generators/` and update `run.py`.
- **Voice Generation**: Implement your custom TTS tool in `tts_transformers/base.py` and integrate it in `run.py`.

By following this approach, you can easily customize the framework to suit your unique requirements, whether it’s pulling data from a specific API, using a different AI model, or leveraging an alternative voice generation service.

---

## 🚀 Quick Start

### 1. **Set Up a Virtual Environment**
Use Python 3.11+ for the framework. Set up a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Unix or MacOS
env\Scripts\activate     # On Windows
```

### 2. **Install Dependencies**
Install dependencies using `pip-tools`:

```bash
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

### 3. **Install FFmpeg**
The framework requires FFmpeg for audio and video processing.

- **macOS**:  
  ```bash
  brew install ffmpeg
  ```
- **Linux (Ubuntu/Debian)**:  
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- **Windows**:  
  [Download FFmpeg](https://ffmpeg.org/download.html), then add the `bin` directory to your PATH.

### 4. **Set Environment Variables**
Configure your environment variables for smooth operation:

- On Unix/MacOS:  
  ```bash
  source env_mac.sh
  ```
- On Windows:  
  ```bash
  env_win.bat
  ```

### 5. **Run the Framework**
Start the framework with a single command:  
```bash
python run.py
```

---

## 🎯 Extendability

The FOMO Radio Framework is built with customization in mind. Feel free to adapt it for:
- Cryptocurrency updates
- Live event coverage
- Personalized content delivery
- Autonomous agents for news or entertainment

---

## ⚠️ Limitations
- Currently supports one show with multiple hosts. Future updates will include multi-show support.

---

## 🛠️ Issues
Encounter any issues or have feature suggestions? Let us know via GitHub Issues!

---

## 📚 Dependencies
Key dependencies include:
- `ffmpeg`
- `mem0ai`

---

## 🤝 Community and Contributions
We welcome contributions and ideas! Join our community and help us improve:

- [GitHub Issues](#): Report bugs or suggest features.
- [Discord](#): Connect with other developers.

---

**Build the future of AI-powered radio with the FOMO Radio Framework!**

