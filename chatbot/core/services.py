# core/services.py
import requests
from django.conf import settings

class GeminiService:
    @staticmethod
    def generate_content(prompt):
        try:
            response = requests.post(
                f"{settings.GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")
    
    

# core/services/conversation_service.py
from api.models import Conversation, Message
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache

class ConversationService:
    @staticmethod
    def get_or_create_conversation(user, session_id):
        """Get or create conversation with caching"""
        cache_key = f"conversation_{session_id}"
        conversation = cache.get(cache_key)
        
        if not conversation:
            if isinstance(user, AnonymousUser):
                user = None
            
            conversation, created = Conversation.objects.get_or_create(
                session_id=session_id,
                defaults={'user': user}
            )
            cache.set(cache_key, conversation, timeout=3600)  # Cache for 1 hour
        
        return conversation
    
    @staticmethod
    def save_message(conversation, user_message, ai_response, domain):
        """Save message with caching"""
        message = Message.objects.create(
            conversation=conversation,
            user_message=user_message,
            ai_response=ai_response,
            domain=domain
        )
        
        # Update conversation cache
        cache_key = f"conversation_{conversation.session_id}"
        cache.set(cache_key, conversation, timeout=3600)
        
        return message
    
    @staticmethod
    def get_conversation_history(session_id, limit=10):
        """Get conversation history with caching"""
        cache_key = f"conversation_history_{session_id}_{limit}"
        messages = cache.get(cache_key)
        
        if not messages:
            try:
                conversation = Conversation.objects.get(session_id=session_id)
                messages = list(conversation.messages.all().order_by('-timestamp')[:limit])
                cache.set(cache_key, messages, timeout=300)  # Cache for 5 minutes
            except Conversation.DoesNotExist:
                messages = []
        
        return messages
    
    @staticmethod
    def clear_conversation(session_id):
        """Clear conversation history"""
        try:
            conversation = Conversation.objects.get(session_id=session_id)
            conversation.messages.all().delete()
            cache.delete_many([
                f"conversation_{session_id}",
                f"conversation_history_{session_id}_*"
            ])
            return True
        except Conversation.DoesNotExist:
            return False