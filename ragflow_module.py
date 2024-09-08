# 使用此版本
# 功能：与RAGFlow进行交互，获取结构化的prompts
import requests

class RAGFlowClient:
    def __init__(self):
        self.base_url = 'http://localhost/v1/'  # 直接在构造函数中设置base_url
        self.api_key = "ragflow-JhMDA0NGY2NmQxZjExZWY4Y2YxMDI0Mm"  # 存储API密钥
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_conversation(self, user_id):
        """
        创建一个新的用户对话会话
        
        Request parameter:
        - user_id (string): The unique identifier assigned to each user. Must be less than 32 characters and cannot be empty.
        
        Response:
        - data.id: The session ID for all upcoming conversations.
        """
        data = {
            "user_id": user_id
        }
        response = requests.get(f"{self.base_url}/api/new_conversation", json=data, headers=self.headers)
        conversation_id = response.json().get('data')['id']  # 保存会话ID
        return conversation_id

    def get_conversation_history(self, conversation_id):
        """
        获取指定会话ID的对话历史
        
        Request parameter:
        - id (string): The unique identifier assigned to a conversation session. Must be less than 32 characters and cannot be empty.
        
        Response:
        - message: All conversations in the specified conversation session.
        - user_id: This is set by the caller.
        - reference: Each reference corresponds to one of the assistant's answers in data.message.
        """
        if conversation_id:
            response = requests.get(f"{self.base_url}/api/conversation/{conversation_id}", headers=self.headers)
            return response.json()
        else:
            return None

    def get_completion(self, user_question, conversation_id):
        """
        从RAGFlow Chat获取用户最新问题的答案
        
        Request parameter:
        - conversation_id (string): The ID of the conversation session.
        - messages (json): The latest question in a JSON form, such as [{"role": "user", "content": "How are you doing!"}]
        - quote (bool): Default: false
        - stream (bool): Default: true
        - doc_ids (string): Document IDs delimited by comma. The retrieved contents will be confined to these documents.
        
        Response:
        - answer: The answer to the user's latest question.
        - reference: The retrieved chunks that contribute to the answer.
        """
        data = {
            "conversation_id": conversation_id,
            "messages": [{"role": "user", "content": user_question}],  # 使用messages参数，列表形式
            "stream": False
        }
        response = requests.post(f"{self.base_url}/api/completion", json=data, headers=self.headers)

        # 尝试解析为JSON
        try:
            return response.json().get('data')['answer']  # 如果返回结果为有效的JSON，进行解析
        except requests.exceptions.JSONDecodeError:
            print("Response is not in JSON format")
            return None

    def get_document(self, document_id):
        """
        检索指定文档ID的内容
        
        Request parameter:
        - id (string): The unique identifier assigned to a document.
        
        Response:
        - The content of the document.
        """
        response = requests.get(f"{self.base_url}/document/get/{document_id}", headers=self.headers)
        return response.json()

    def upload_document(self, document_data):
        """
        上传特定文件到指定知识库
        
        Request parameter:
        - file (file): The file to upload.
        - kb_name (string): The name of the knowledge base to upload the file to.
        - parser_id (string): The parsing method (chunk template) to use. Default: 'naive'.
        - run (string): 1: Automatically start file parsing. Default: '0'.
        
        Response:
        - The result of the upload operation.
        """
        response = requests.post(f"{self.base_url}/api/document/upload", json=document_data, headers=self.headers)
        return response.json()

    def list_chunks(self, document_id):
        """
        通过文档名称或ID检索特定文档的块
        
        Request parameter:
        - doc_name (string): The name of the document in the knowledge base. It must not be empty if doc_id is not set.
        - doc_id (string): The ID of the document in the knowledge base. It must not be empty if doc_name is not set.
        
        Response:
        - The chunks of the specified document.
        """
        response = requests.get(f"{self.base_url}/api/list_chunks?document_id={document_id}", headers=self.headers)
        return response.json()

    def list_kb_docs(self, knowledge_base_id):
        """
        从指定知识库获取文档列表
        
        Request parameter:
        - kb_name (string): The name of the knowledge base, from which you get the document list.
        - page (int): The number of pages. Default: 1.
        - page_size (int): The number of docs for each page. Default: 15.
        - orderby (string): chunk_num, create_time, or size. Default: create_time.
        - desc (bool): Default: True.
        - keywords (string): Keyword of the document name.
        
        Response:
        - The list of documents in the specified knowledge base.
        """
        payload = {
            "knowledge_base_id": knowledge_base_id
        }
        response = requests.post(f"{self.base_url}/api/list_kb_docs", json=payload, headers=self.headers)
        return response.json()

    def delete_document(self, document_id):
        """
        通过文档ID或名称删除文档
        
        Request parameter:
        - doc_names (List): A list of document names. It must not be empty if doc_ids is not set.
        - doc_ids (List): A list of document IDs. It must not be empty if doc_names is not set.
        
        Response:
        - The result of the delete operation.
        """
        response = requests.delete(f"{self.base_url}/api/document", json={"id": document_id}, headers=self.headers)
        return response.json()

def use_case1():
    ragflow_client = RAGFlowClient()
    
    # 创建新的对话会话
    user_id = "test_user_id_2004"
    conversation_id = ragflow_client.create_conversation(user_id)
    print("新对话会话:", conversation_id)

    # 获取对话历史
    history = ragflow_client.get_conversation_history(conversation_id)
    print("对话历史:", history)

    # 获取问题的答案
    user_question = "请告诉我关于产品的信息。"
    completion = ragflow_client.get_completion(user_question, conversation_id)
    print("问题答案:", completion)


def use_case2():    
    # 示例用法
    ragflow_client = RAGFlowClient()
    
    # 创建新的对话会话
    user_id = "test_user_id_2004"
    conversation_id = ragflow_client.create_conversation(user_id)
    print("新对话会话ID:", conversation_id)

    # 持续沟通
    while True:
        user_question = input("请输入您的问题（输入'退出'结束）：")
        if user_question.lower() == 'q':
            break
        
        # 获取问题的答案
        completion = ragflow_client.get_completion(user_question, conversation_id)
        print("问题答案:", completion)
        
        # # 可选：获取对话历史
        # history = ragflow_client.get_conversation_history(conversation_id)
        # print("对话历史:", history)

def use_case3():
    # 示例用法
    ragflow_client = RAGFlowClient()
    conversation_id = '47a535326b5411efb1070242ac120006'
    history = ragflow_client.get_conversation_history(conversation_id)
    print("对话历史:", history)

if __name__ == "__main__":
    use_case3()
