# 功能：存储和管理历史会话数据
from pymongo import MongoClient
from datetime import datetime

class ConversationManager:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['customer_service']
        self.collection = self.db['history_conversations']

    def insert_conversation(self, user_id, platform, user_message, assistant_message):
        """
        插入一条对话记录到history_conversations集合中

        Parameters:
        - user_id (str): 用户的唯一标识符
        - platform (str): 对话发生的平台
        - user_message (str): 用户的消息
        - assistant_message (str): 助手的回复
        """
        conversation = {
            'user_id': user_id,
            'platform': platform,
            'time': datetime.now(),
            'interaction': {
                'user': user_message,
                'assistant': assistant_message
            }
        }
        self.collection.insert_one(conversation)

    def get_user_history(self, user_id, platform, max_count, max_tokens):
        """
        获取用户历史会话

        Parameters:
        - user_id (str): 用户的唯一标识符
        - platform (str): 对话发生的平台
        - max_count (int): 指定的最多获取的次数
        - max_tokens (int): 指定的最大的tokens数

        Returns:
        - list: 用户历史会话记录,示例 {'user':user_message,"assistant":assistant_message}
        """
        query = {'user_id': user_id, 'platform': platform}
        docs = self.collection.find(query).sort('time', -1).limit(max_count)
        
        conversations = []
        total_tokens = 0

        for doc in docs:
            user_message = doc['interaction']['user']
            assistant_message = doc['interaction']['assistant']
            tokens = len(user_message) + len(assistant_message)
            
            if total_tokens + tokens > max_tokens:
                break
            
            converstaion = {'user':user_message,"assistant":assistant_message}
            conversations.append(converstaion)
            total_tokens += tokens

        return conversations

def test_insert_conversations():
    """
    测试函数，用于插入几条对话记录
    """
    manager = ConversationManager()
    conversations = [
        {
            'user_id': 'user_123', 
            'platform': 'taobao', 
            'user_message': 'Hello, how can I help you?', 
            'assistant_message': 'I need help with my order.'
        },
        {
            'user_id': 'user_123', 
            'platform': 'jd', 
            'user_message': 'Sure, I can assist you with that.', 
            'assistant_message': 'Thank you!'
        }
    ]
    
    for conv in conversations:
        manager.insert_conversation(conv['user_id'], conv['platform'], conv['user_message'], conv['assistant_message'])

if __name__ == "__main__":
    test_insert_conversations()
    print("测试数据已插入")
