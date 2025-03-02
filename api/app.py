from flask import Flask, render_template, request, jsonify
from src.reasoning.engine import ReasoningEngine
import logging

app = Flask(__name__)
engine = ReasoningEngine()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json.get('question', '')
        if not question:
            return jsonify({'error': 'Please ask a question'}), 400
        
        # Process the question
        result = engine.reason(question)
        
        # Format the response
        response = {
            'sources': [
                {
                    'reference': source.reference,
                    'text': source.text,
                    'context': source.context,
                    'chapter': source.metadata.get('chapter', '')
                }
                for source in result.relevant_sources
            ],
            'reasoning': result.reasoning,
            'confidence': float(result.confidence_score)  # Convert numpy.float32 to Python float
        }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred processing your question'}), 500

if __name__ == '__main__':
    app.run(debug=False) 