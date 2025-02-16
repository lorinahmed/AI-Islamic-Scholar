# Islamic AI Assistant

An AI-powered assistant that uses the Quran to reason about Islamic questions using RAG (Retrieval Augmented Generation) and analogical reasoning (Qiyas).

## Features
- RAG-based retrieval of relevant Quranic verses
- Context-aware verse analysis
- Analogical reasoning using Islamic principles
- Confidence scoring based on relevance
- Versioned FAISS index for efficient retrieval

## Setup
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/islamic-ai-assistant.git
   cd islamic-ai-assistant
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Prepare the data
   ```bash
   # Download and prepare the Quran data
   python scripts/prepare_data.py
   # This will:
   # 1. Download the Quran data if not already present
   # 2. Create the data directory if needed
   # The FAISS index will be created automatically when you first run the application
   ```

5. Create a `.env` file with your OpenAI API key
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

6. Run the application
   ```bash
   python main.py
   ```

## Data
The project requires a `quran.json` file in the `data` directory. This file should contain the Quran verses with their metadata in the following format:
```json
{
  "verses": [
    {
      "reference": "1:1",
      "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful",
      "topics": ["mercy", "divinity"],
      "principles": ["tawhid", "mercy"]
    },
    ...
  ]
}
```

## Project Structure

```
islamic-ai-assistant/
├── data/
│   ├── quran.json
│   └── .gitkeep
├── src/
│   ├── models/
│   │   └── data_models.py
│   ├── reasoning/
│   │   └── engine.py
│   └── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## License
MIT License

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate.

## Note
This project is for educational purposes and should not be used as a substitute for proper Islamic scholarship. Always consult with qualified Islamic scholars for religious guidance.