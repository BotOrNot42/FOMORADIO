
# FOMO Radio Framework 🎙️

The FOMO Radio Framework is designed to revolutionize content consumption by combining AI, real-time data aggregation, and voice synthesis. Whether you're building autonomous radio stations or creating personalized audio summaries, this framework empowers you to deliver intelligent, engaging, and tailored audio experiences.

---

## Architecture and Design

The framework operates through four primary stages:
1. **Data Collection**
2. **Script Generation**
3. **TTS Transformers**
4. **Content Delivery**
   

The dynamic architecture ensures **flexibility**, **modularity**, and **scalability** for a variety of use cases.
![Rough Chart - Experience](https://github.com/user-attachments/assets/25db07ca-16bc-4572-9404-e758425954b0)

---

## Features

### **AI-Powered Content Aggregation (Data Collectors)**
Seamlessly gather data from diverse platforms.

### **Dynamic Memory Management (Core)**
Leverages `mem0` for maintaining contextual relevance.

### **Automatic Summarization (Script Generators)**
Converts raw data into structured, audience-ready summaries.

### **Multimedia Output (TTS Transformers)**
Generates audio and video summaries, ready for distribution across platforms.

### **Export Capabilities (Consumers)**
Distributes summaries and multimedia files to social media, streaming services, or custom destinations.

---

## 💡 Use Cases

The FOMO Radio Framework is designed with adaptability and customization at its core, enabling developers to modify and extend it for a wide range of use cases. Below are just a few possibilities to inspire your next project:

- **Crypto News Updates**:  
  Create real-time audio feeds for crypto enthusiasts by aggregating data from platforms like Twitter, Telegram, and news sources to deliver market trends, token updates, and trading insights.

- **Live Event Coverage**:  
  Stream AI-powered, play-by-play commentary for sports, conferences, or breaking news events by integrating live data feeds.

- **Personalized Content Delivery**:  
  Build personalized AI companions that curate, summarize, and narrate news, social media trends, or market insights tailored to individual users' preferences.

- **Autonomous News Agents**:  
  Develop unbiased, fully automated news channels that aggregate, verify, and synthesize content from multiple sources to deliver fact-based, engaging audio summaries.

- **Entertainment Radio Stations**:  
  Create interactive, themed radio shows for entertainment niches such as memes, movie reviews, or celebrity updates.

The framework’s modular structure allows seamless integration of new data sources, AI models, or voice synthesis tools to suit your unique needs.

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

### 📚 Dependencies
Key dependencies include:
- `ffmpeg`
- `mem0ai`

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

## ⚠️ Limitations

The current version of the framework supports one show with multiple hosts. While this setup is ideal for focused use cases, future updates will expand functionality to support multi-show environments, enabling the creation of diverse programming schedules.

For now, certain features such as multilingual support and large-scale simultaneous data processing are in development, with enhancements planned for upcoming releases.

---

## 🛠️ Issues and Suggestions

Your feedback is invaluable! If you encounter any issues, have suggestions for improvement, or want to share a new feature idea, please don’t hesitate to connect with us. You can:

- **Report Bugs**: Use the [GitHub Issues tab](https://github.com/BotOrNot42/FOMORADIO/issues) to let us know about any problems you face.
- **Request Features**: Suggest new capabilities or improvements to make the framework even better.
- **Contribute to Development**: Join the community of developers working to refine and expand the FOMO Radio Framework.

Together, we can shape the future of autonomous, AI-driven content delivery.

---

**Build the future of AI-powered radio with the FOMO Radio Framework!**

