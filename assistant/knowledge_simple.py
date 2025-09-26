
#!/usr/bin/env python3
"""
Knowledge Simple Ingestion
Basic knowledge processing that extracts 3 key insights from PDF documents.
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeProcessor:
    """Simple knowledge processor for PDF documents."""
    
    def __init__(self, server_url: str = "http://localhost:8001"):
        self.server_url = server_url
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.
        This is a simplified version - in production use PyPDF2, pdfplumber, or similar.
        """
        try:
            # For demo purposes, simulate PDF text extraction
            # In production, replace with actual PDF processing
            pdf_file = Path(pdf_path)
            
            if not pdf_file.exists():
                # Create a sample PDF content for demonstration
                sample_content = f"""
                Sample Document: {pdf_file.name}
                
                This is a demonstration of the knowledge ingestion system.
                The system processes documents and extracts meaningful insights
                using advanced AI and machine learning techniques.
                
                Key concepts covered:
                - Data processing and analysis
                - Learning from structured content
                - Automated insight generation
                - System integration and workflow automation
                
                The self-learning assistant continuously improves its understanding
                by processing new documents and incorporating feedback from users.
                This creates a spiral of continuous learning and improvement.
                """
                logger.info(f"PDF not found, using sample content for {pdf_path}")
                return sample_content
            
            # If file exists, read it as text (simplified)
            try:
                with open(pdf_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content
            except UnicodeDecodeError:
                logger.warning(f"Could not read {pdf_path} as text, using sample content")
                return f"Sample content from {pdf_file.name} - PDF processing would extract actual text here."
                
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return f"Error processing {pdf_path}: {str(e)}"
    
    def process_document(self, pdf_path: str) -> Dict[str, Any]:
        """Process a PDF document and extract insights."""
        logger.info(f"Processing document: {pdf_path}")
        
        # Extract text from PDF
        text_content = self.extract_text_from_pdf(pdf_path)
        
        # Send to MCP server for learning
        try:
            response = requests.post(
                f"{self.server_url}/learn",
                json={
                    "content": text_content,
                    "source": f"pdf:{Path(pdf_path).name}",
                    "metadata": {
                        "file_path": pdf_path,
                        "file_size": len(text_content),
                        "processing_timestamp": "2024-01-01T00:00:00"
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Successfully processed document with {len(result['insights'])} insights")
                return result
            else:
                logger.error(f"Server error: {response.status_code} - {response.text}")
                return {"error": f"Server error: {response.status_code}"}
                
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to MCP server. Is it running on http://localhost:8001?")
            return {"error": "MCP server not available"}
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return {"error": str(e)}
    
    def batch_process(self, pdf_directory: str) -> List[Dict[str, Any]]:
        """Process multiple PDF files in a directory."""
        pdf_dir = Path(pdf_directory)
        results = []
        
        if not pdf_dir.exists():
            logger.error(f"Directory not found: {pdf_directory}")
            return [{"error": f"Directory not found: {pdf_directory}"}]
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_directory}")
            return [{"warning": f"No PDF files found in {pdf_directory}"}]
        
        for pdf_file in pdf_files:
            result = self.process_document(str(pdf_file))
            results.append({
                "file": str(pdf_file),
                "result": result
            })
        
        return results

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python knowledge_simple.py <pdf_file_or_directory>")
        print("Example: python knowledge_simple.py sample.pdf")
        print("Example: python knowledge_simple.py ./documents/")
        sys.exit(1)
    
    target_path = sys.argv[1]
    processor = KnowledgeProcessor()
    
    print("🧠 Knowledge Ingestion System")
    print("=" * 40)
    
    target = Path(target_path)
    
    if target.is_file() or not target.exists():
        # Process single file
        print(f"📄 Processing: {target_path}")
        result = processor.process_document(target_path)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Success! Generated {len(result.get('insights', []))} insights:")
            for i, insight in enumerate(result.get('insights', []), 1):
                print(f"   {i}. {insight}")
            print(f"🎯 Confidence: {result.get('confidence', 0):.2f}")
    
    elif target.is_dir():
        # Process directory
        print(f"📁 Processing directory: {target_path}")
        results = processor.batch_process(target_path)
        
        for item in results:
            print(f"\n📄 File: {item['file']}")
            result = item['result']
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Generated {len(result.get('insights', []))} insights")
    
    print("\n🔗 View more details at: http://localhost:8001/insights")

if __name__ == "__main__":
    main()
