
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
   ElevenLabs is used for generating high-quality, natural-sounding voice outputs.

### How to Use Alternative Services
If you'd like to use other data collection sources, AI models, or voice generation tools, you'll need to make changes to the following files:

1. **Data Collection (Twitter v2 API)**:  
   Update the integration logic in the `data_collection.py` file. Replace Twitter API endpoints with your preferred data source APIs.

2. **AI Models (OpenAI)**:  
   Modify the AI model integration in `ai_processing.py`. Replace the OpenAI API calls with the corresponding SDK or API calls for your desired AI service.

3. **Voice Generation (ElevenLabs)**:  
   Update the voice synthesis logic in `voice_generation.py`. Replace ElevenLabs API calls with your preferred text-to-speech service.

### Example:
If you're replacing Twitter API with a news API:  
1. Replace the Twitter API fetch logic in `data_collection.py` with requests to the news API.
2. Adjust the data parsing logic to match the new API's response format.

If you're switching to another AI model like **Anthropic** or **Llama**:  
1. Update API calls in `ai_processing.py` to integrate the alternative AI model.
2. Ensure the prompt structure is compatible with the new model.

If you're switching to another voice generation tool like **Amazon Polly**:  
1. Update the `voice_generation.py` file to use Amazon Polly’s SDK or API.  
2. Adjust settings like voice type, language, and speed to match your requirements.

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

