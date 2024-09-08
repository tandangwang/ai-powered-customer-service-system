# 功能：协调MongoDB和RAGFlow的API调用，处理整个流程

from mongodb_module import ConversationManager
from ragflow_module import RAGFlowClient
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.chat_message_histories import ChatMessageHistory
import re
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class ConversationHandler:
    def __init__(self):
        self.mongodb_manager = ConversationManager()
        self.ragflow_client = RAGFlowClient()
        self.conversations_history = []
        self.user_id = None
        self.platform = None
        self.cleaned_user_input = None
        # whether is first converstion in this session
        self.is_fist_converstion = True

        self.conversation_id = None
        self.model = Ollama(model="glm4:latest")
        self.chat_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use the following information to respond to the user's query. Please keep your response within 500 tokens."),
            ("user", "{history}"),
            ("user", "RAG Results: {rag_results}\nPlease provide a response based on all available information."),
        ])
        self.chat_history = ChatMessageHistory(chain=self.model)

    def extract_user_info(self, user_input):
        user_id_match = re.search(r'user_id:\s*(\w+)', user_input)
        platform_match = re.search(r'platform:\s*(\w+)', user_input)
        self.user_id = user_id_match.group(1) if user_id_match else "user_123"
        self.platform = platform_match.group(1) if platform_match else "taobao"


    def initialize_conversation(self):
        # Retrieve the user's message history from MongoDB
        self.conversations_history = self.mongodb_manager.get_user_history(self.user_id, self.platform, max_count=5, max_tokens=1000)
        # Create a new conversation in RAGFlow and get the conversation ID
        self.conversation_id = self.ragflow_client.create_conversation(self.user_id)

    def process_user_input(self, user_input):
        # Extract user information from the input and clean it, return pure message without id and platform
        if not self.user_id:
            self.extract_user_info(user_input)
            self.initialize_conversation()
        cleaned_input = user_input.replace(f"user_id: {self.user_id}", "").replace(f"platform: {self.platform}", "").strip()
        self.cleaned_user_input = cleaned_input
        return cleaned_input

    def get_rag_results(self,user_input):
        return self.ragflow_client.get_completion(user_input, self.conversation_id)

    def update_mongodb(self,user_input,llm_output):
        self.mongodb_manager.insert_conversation(self.user_id,self.platform,user_input,llm_output)

    def generate_response(self, rag_results):       
        messages = []
        
        # Add system message
        system_prompt = """
            You are a helpful assistant. Use the following information to respond to the user's query. 
            Please keep your response within 500 tokens.
            Answer in Chinese.
        """
        messages.append(SystemMessage(content=system_prompt))
        
        # Add history if it's the first conversation
        if self.is_fist_converstion:
            self.is_fist_converstion = False            
            for conversation in self.conversations_history:          
                messages.append(HumanMessage(content=conversation['user']))
                messages.append(AIMessage(content=conversation['assistant']))
        
        # Add RAG results
        messages.append(HumanMessage(content=f"RAG Results: {rag_results}\nPlease provide a response based on all available information."))
        
        # Invoke the model with the formatted messages
        response = self.model.invoke(messages)
        
        # Process the response
        if isinstance(response, str):
            response_text = response
        elif isinstance(response, dict) and "content" in response:
            response_text = response["content"]
        else:
            response_text = str(response)  # Fallback to string conversion if structure is unknown
        
        self.update_mongodb(self.cleaned_user_input, response_text)
        
        return response_text

    def handle_conversation(self, user_input):
        cleaned_input = self.process_user_input(user_input)
        rag_results = self.get_rag_results(cleaned_input)
        response_text = self.generate_response(rag_results)
        return response_text


def main():
    handler = ConversationHandler()
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            break
        
        response = handler.handle_conversation(user_input)
        print("Assistant:", response,end="\n\n")

if __name__ == "__main__":
    main()