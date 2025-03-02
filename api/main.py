from src.reasoning.engine import ReasoningEngine
from src.models.data_models import IslamicSource
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize the reasoning engine
        engine = ReasoningEngine()
        
        print("\nWelcome to the Islamic AI Assistant!")
        print("You can ask questions about Islamic topics. Type 'quit' to exit.\n")
        
        while True:
            # Get user input
            question = input("\nYour question: ").strip()
            
            # Check for exit command
            if question.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Islamic AI Assistant. Goodbye!")
                break
                
            # Skip empty questions
            if not question:
                print("Please ask a question.")
                continue
            
            # Process the question
            result = engine.reason(question)
            
            # Print the response in a formatted way
            print("\nRelevant Sources with Context:")
            for source in result.relevant_sources:
                print(f"\nMain verse: {source.reference}")
                print(f"Text: {source.text}")
                print("\nSurrounding verses (Context):")
                for ref, text in source.context.items():
                    print(f"{ref}: {text}")
                print("\nChapter:", source.metadata['chapter'])
            
            print("\nReasoning:")
            print(result.reasoning)
            
            print(f"\nConfidence Score: {result.confidence_score}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main() 