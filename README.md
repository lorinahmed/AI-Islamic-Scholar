# Islamic AI Assistant

An AI-powered assistant that uses the Quran to reason about Islamic questions using RAG (Retrieval Augmented Generation) and analogical reasoning (Qiyas).

## Project Structure
```
islamic-ai-assistant/
├── api/                    # Backend API
│   ├── src/               # Source code
│   │   ├── reasoning/     # Core reasoning engine
│   │   └── models/        # Data models
│   ├── scripts/           # Utility scripts
│   ├── data/              # Data files
│   ├── requirements.txt   # Python dependencies
│   └── main.py           # API entry point
├── web/                   # Frontend application
│   ├── src/              # React source code
│   ├── public/           # Static files
│   └── package.json      # Node dependencies
└── README.md
```

## Backend Setup
1. Navigate to the API directory:
   ```bash
   cd api
   ```

2. Follow the setup instructions in `api/README.md`

## Frontend Setup
1. Navigate to the web directory:
   ```bash
   cd web
   ```

2. Follow the setup instructions in `web/README.md`

## Development
- Backend API runs on http://localhost:5000
- Frontend development server runs on http://localhost:3000

## Contributing
See CONTRIBUTING.md for guidelines.

## Features
- RAG-based retrieval of relevant Quranic verses
- Context-aware verse analysis
- Analogical reasoning using Islamic principles
- Efficient vector search using FAISS
- Contextual verse understanding

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

## License
MIT License

## Note
This project is for educational purposes and should not be used as a substitute for proper Islamic scholarship. Always consult with qualified Islamic scholars for religious guidance.