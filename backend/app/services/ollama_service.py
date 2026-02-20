"""
Ollama LLM Service
Integrates local Ollama model for intelligent chat responses
"""
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


class OllamaService:
    """Service for interacting with local Ollama LLM model"""
    
    # Initialize the model once
    _model = None
    _prompt_template = None
    
    @classmethod
    def _initialize(cls):
        """Initialize the Ollama model and prompt template"""
        if cls._model is None:
            try:
                cls._model = OllamaLLM(model="llama3")
                
                # Housing law specialized prompt template
                cls._prompt_template = ChatPromptTemplate.from_template("""
You are HomeRights AI, an expert UK housing law advisor. You provide clear, accurate, and empathetic advice to tenants about their rights.

Context from previous conversation:
{context}

Current question: {question}

Instructions:
- Provide accurate information based on UK housing law (including the Renters Rights Act 2025)
- Be empathetic and supportive
- Use clear, simple language
- Include specific legal references when relevant
- Suggest actionable next steps
- Mention relevant support organizations (Shelter, Citizens Advice) when appropriate
- Format your response with clear sections using markdown-style formatting
- If analyzing a document, identify potential issues and explain their significance

Answer:
""")
                
                print("✅ Ollama LLM initialized successfully with llama3 model")
            except Exception as e:
                print(f"❌ Failed to initialize Ollama LLM: {e}")
                print("Make sure Ollama is running and llama3 model is installed")
                print("Run: ollama pull llama3")
                raise
    
    @classmethod
    def generate_response(cls, question: str, context: str = "") -> str:
        """
        Generate a response using the Ollama LLM
        
        Args:
            question: The user's question or message
            context: Previous conversation context
            
        Returns:
            Generated response string
        """
        cls._initialize()
        
        try:
            # Create the chain
            chain = cls._prompt_template | cls._model
            
            # Generate response
            result = chain.invoke({
                "context": context,
                "question": question
            })
            
            return result
            
        except Exception as e:
            print(f"Error generating response with Ollama: {e}")
            # Fallback to a helpful error message
            return (
                "I apologize, but I'm having trouble connecting to my AI model right now. "
                "This might be because:\n\n"
                "• The Ollama service isn't running\n"
                "• The llama3 model isn't installed\n\n"
                "Please contact support or try again later. In the meantime, you can:\n"
                "• Call Shelter: 0808 800 4444\n"
                "• Call Citizens Advice: 0800 144 8848"
            )
    
    @classmethod
    def generate_document_analysis(cls, document_text: str, detected_issues: list = None) -> str:
        """
        Generate a detailed document analysis using the LLM
        
        Args:
            document_text: The document text to analyze
            detected_issues: List of issues detected by ML service
            
        Returns:
            Detailed analysis response
        """
        cls._initialize()
        
        try:
            # Build context with detected issues
            issues_context = ""
            if detected_issues:
                issues_context = "\n\nDetected Issues:\n"
                for issue in detected_issues:
                    issues_context += f"- {issue['issue']}: {issue['explanation']}\n"
            
            question = f"""
Please analyze this tenancy document and provide a comprehensive review:

Document Text:
{document_text[:2000]}...

{issues_context}

Provide:
1. Overall assessment of fairness
2. Explanation of concerning clauses
3. Tenant's rights and protections
4. Recommended actions
"""
            
            return cls.generate_response(question, "")
            
        except Exception as e:
            print(f"Error analyzing document with Ollama: {e}")
            return "I apologize, but I'm having trouble analyzing this document right now. Please try again later."
    
    @classmethod
    def build_conversation_context(cls, conversation_history: list) -> str:
        """
        Build context string from conversation history
        
        Args:
            conversation_history: List of previous messages
            
        Returns:
            Formatted context string
        """
        if not conversation_history:
            return ""
        
        context = ""
        # Get last 5 messages for context (to avoid token limits)
        recent_messages = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        
        for msg in recent_messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            if role == 'user':
                context += f"\nUser: {content}"
            elif role == 'assistant':
                context += f"\nAI: {content}"
        
        return context
