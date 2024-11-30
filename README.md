# FOMO Framework

The FOMO Framework is designed to aggregate content from multiple sources, analyze it using the `mem0` library, and maintain a dynamic memory system. It can recall information based on the latest content and user interactions, and automatically summarize this information in a pre-structured format. Additionally, the framework is capable of generating audio and video files from summaries and exporting them to various platforms.

## Specialities
1. **Content Aggregation:** Framework is designed to gather and analyze content from multiple sources efficiently.

2. **Memory Management:** Utilizes the `mem0` library to maintain a dynamic memory system that recalls information based on new content and user interactions.

3. **Automatic Summarization:** Automatically structures and summarizes the information it processes, preparing it for further use or dissemination.

4. **Multimedia Output:** Capable of generating both audio and video files from the summarized content, enhancing the accessibility and applicability of the output.

5. **Export Capabilities:** Exports the processed summaries and multimedia files to various platforms, supporting broad distribution.

## Setup Instructions

### Creating a Virtual Environment

It is recommended to use Python version 3.11 or higher for this framework. You can set up a virtual environment using the following commands:

\```bash
python -m venv venv
source venv/bin/activate  # On Unix or MacOS
venv\\Scripts\\activate  # On Windows
\```

### Installing Dependencies

First, install `pip-tools` for dependency management:

\```bash
pip install pip-tools
\```

Compile and install all dependencies using `pip-compile` and `pip`:

\```bash
pip-compile requirements.in
pip install -r requirements.txt
\```

### Installing FFmpeg

FFmpeg is required for handling audio and video files. Here's how you can install it on different operating systems:

- **macOS**:
  \```bash
  brew install ffmpeg
  \```

- **Linux (Ubuntu/Debian)**:
  \```bash
  sudo apt update
  sudo apt install ffmpeg
  \```

- **Windows**:
  Download the static builds from the FFmpeg website, then add the `bin` directory to your system’s PATH.

## Known Limitations

Currently, the framework supports only one show with multiple hosts. Future versions are planned to extend support to multiple shows.

## Dependencies

Ensure the following dependencies are included in your `requirements.txt`:

- mem0
- ffmpeg-python
- Any other libraries your project requires