## News Reader

This project will combine news articles from public RSS feeds and generate a voice summary of the key points. The summary is generated using [ollama](https://ollama.com/). The voiceover is generated using [kokoro](https://github.com/hexgrad/kokoro).

## Limitations
- The accuracy of the summary depends on the quality of the RSS feeds and the model in use by ollama.
- The voiceover might have trouble with some names or terms, especially those that are not common or have specific pronunciations.

## Requirements
- A computer capable of running a small Ollama model and Kokoro.

## Installation
```
git clone https://github.com/Tumppi066/news-reader.git
cd news-reader
pip install -r requirements.txt
```

## Usage
Just run `python main.py` in the source directory and the script will fetch the latest articles. This project has no user interface, so you will have to modify the `rss.py` file if you want to change RSS feeds. You can change the model in the `summary.py` file.

## Example
Below is an audio file with the default RSS feeds and the default model (`gemma3:4b`).

[Example Audio](examples/example-11-06-25.mp3)