# English Vocabulary Pipeline

Automation pipeline for building an English vocabulary dataset from online sources.

## 🚀 Features
- Scrapes word lists from **Cambridge Dictionary**
- Extracts definitions and parts of speech
- Collects **UK / US IPA transcriptions**
- Translates words using **DeepL**
- Saves structured data to JSON files

## 🛠 Tech Stack
- Python 3
- Playwright (async)
- Patchright
- JSON

## 📂 Pipeline Overview
1. `cambridge_parse.py` — parses word lists from Cambridge Dictionary  
2. `transcript_parse.py` — adds UK/US IPA pronunciation  
3. `deepl_translate.py` — translates words via DeepL  

## ▶️ Usage
```bash
python cambridge_parse.py
python transcript_parse.py
python deepl_translate.py
