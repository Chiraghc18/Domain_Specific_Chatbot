# api/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.domains import get_domain_handler  # Your domain detection function
from core.services import GeminiService, ConversationService
import markdown
from bs4 import BeautifulSoup
import uuid
from django.contrib.auth.models import AnonymousUser

import traceback

@api_view(['POST'])
@permission_classes([AllowAny])
def chat(request):
    try:
        user_message = request.data.get('message', '').strip()
        if not user_message:
            return Response({"error": "Message cannot be empty"}, status=400)

        # Get or create session ID
        session_id = request.headers.get('X-Session-ID', str(uuid.uuid4()))
        
        # Get conversation and history
        conversation = ConversationService.get_or_create_conversation(
            request.user if hasattr(request, 'user') and request.user.is_authenticated else AnonymousUser(),
            session_id
        )
        history = ConversationService.get_conversation_history(session_id, limit=5)
        
        # Detect domain and generate response
        domain = get_domain_handler(user_message)
        prompt = domain.generate_prompt(user_input=user_message, conversation=conversation)
        raw_response = GeminiService.generate_content(prompt)
        processed_response = domain.process_output(raw_response)
        
        # Save to database
        ConversationService.save_message(
            conversation=conversation,
            user_message=user_message,
            ai_response=processed_response,
            domain=domain.name
        )
        
        # Convert to HTML and sanitize
        html_response = markdown.markdown(processed_response)
        soup = BeautifulSoup(html_response, 'html.parser')
        
        allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'a']
        for tag in soup.find_all(True):
            if tag.name not in allowed_tags:
                tag.unwrap()
            elif tag.name == 'a':
                tag.attrs['target'] = '_blank'
                tag.attrs['rel'] = 'noopener noreferrer'

        return Response({
            "reply": str(soup),
            "domain": domain.name,
            "session_id": session_id
        })

    except Exception as e:
        print("Exception in /api/chat/:", str(e))
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def clear_conversation(request):
    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return Response({"error": "Session ID required"}, status=400)
    
    success = ConversationService.clear_conversation(session_id)
    return Response({"success": success})