import os
import json
import asyncio
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv() 

# Initialize Anthropic client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Define our tools
tools = [
    {
        "name": "search_youtube_videos",
        "description": "Searches YouTube for Toki Pona learning videos matching the query. Use this when the student wants to find videos about specific Toki Pona topics or lessons.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query related to Toki Pona, e.g., 'toki pona basics', 'toki pona grammar'"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_video_content",
        "description": "Retrieves the transcript and metadata for a specific YouTube video. Use this when the student has selected a video to learn from.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "YouTube video ID, a unique identifier for the video"
                }
            },
            "required": ["video_id"]
        }
    }
]

# Function implementations
def search_youtube_videos(query):
    """Prototype implementation - returns mock data"""
    print(f"[SYSTEM] Searching YouTube for: {query}")
    # Mock data for quick testing
    return [
        {
            "id": "video123",
            "title": "Toki Pona Basics - Lesson 1",
            "channel": "Toki Pona Academy",
            "duration": "10:15",
            "description": "Introduction to Toki Pona language basics"
        },
        {
            "id": "video456",
            "title": "Learn Toki Pona in 12 Minutes",
            "channel": "Language Explorer",
            "duration": "12:01",
            "description": "Quick introduction to the minimalist language"
        }
    ]

def get_video_content(video_id):
    """Prototype implementation - returns mock data"""
    print(f"[SYSTEM] Retrieving content for video: {video_id}")
    # Mock transcript for quick testing
    return {
        "title": "Toki Pona Basics - Lesson 1" if video_id == "video123" else "Learn Toki Pona in 12 Minutes",
        "channel": "Toki Pona Academy" if video_id == "video123" else "Language Explorer",
        "transcript": "toki! ni li pona. mi jan Mark. mi pana e sona pi toki pona. toki pona li pona. ona li lili. ona li jo e nimi lili. nimi ali li pona...",
        "published_at": "2023-05-15",
        "has_subtitles": True,
        "language": "toki pona + english"
    }

# Function registry
function_registry = {
    "search_youtube_videos": search_youtube_videos,
    "get_video_content": get_video_content
}

class SimpleSession:
    def __init__(self):
        self.search_results = None
        self.current_video_id = None
        self.current_content = None
        self.conversation_history = []
    
    def add_user_message(self, content):
        self.conversation_history.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        self.conversation_history.append({"role": "assistant", "content": content})

async def chat_with_toki_pona_assistant(user_message, session):
    """Process a user message with the Toki Pona assistant"""
    
    # Add the user message to the conversation history
    session.add_user_message(user_message)
    
    # Include transcript context if available
    transcript_context = ""
    if session.current_content:
        transcript_context = f"\nCurrent video: {session.current_content['title']} by {session.current_content['channel']}\n\nTranscript: {session.current_content['transcript']}"
    
    # Call Claude with tools
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system="You are a helpful Toki Pona learning assistant that guides students through learning Toki Pona using YouTube videos. You can search for relevant videos and retrieve their content to help students learn." + transcript_context,
        messages=session.conversation_history[-10:],  # Keep last 10 messages
        tools=tools
    )
    
    # Check for tool use
    if hasattr(response, 'content') and response.content and len(response.content) > 0:
        for content_item in response.content:
            if content_item.type == "tool_use":
                tool_use = content_item
                function_name = tool_use.name
                
                # Parse input if it's a string, otherwise use as is
                if isinstance(tool_use.input, str):
                    function_args = json.loads(tool_use.input)
                else:
                    function_args = tool_use.input
                
                print(f"[SYSTEM] Function call: {function_name}({function_args})")
                
                # Call the appropriate function
                if function_name in function_registry:
                    function_result = function_registry[function_name](**function_args)
                    
                    # Update session
                    if function_name == "search_youtube_videos":
                        session.search_results = function_result
                    elif function_name == "get_video_content":
                        session.current_video_id = function_args.get("video_id")
                        session.current_content = function_result
                    
                    # Store assistant's tool use message
                    session.add_assistant_message([
                        {"type": "tool_use", "id": tool_use.id, "name": tool_use.name, "input": tool_use.input}
                    ])
                    
                    # Store user's tool result message - use json.dumps for the content
                    session.add_user_message([
                        {"type": "tool_result", "tool_use_id": tool_use.id, "content": json.dumps(function_result)}
                    ])
                    
                    # Get final response with function results
                    final_response = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1024,
                        system="You are a helpful Toki Pona learning assistant that guides students through learning Toki Pona using YouTube videos." + transcript_context,
                        messages=session.conversation_history[-10:]
                    )
                    
                    # Extract and store the text response
                    if hasattr(final_response, 'content') and final_response.content:
                        for content_item in final_response.content:
                            if content_item.type == "text":
                                response_text = content_item.text
                                session.add_assistant_message(response_text)
                                return response_text
    
    # Handle regular text response
    if hasattr(response, 'content') and response.content:
        for content_item in response.content:
            if content_item.type == "text":
                response_text = content_item.text
                session.add_assistant_message(response_text)
                return response_text
    
    return "I'm having trouble processing your request right now."

async def main():
    session = SimpleSession()
    
    print("Toki Pona Learning Assistant")
    print("Type 'exit' to quit")
    print("\nAssistant: Hi! I can help you learn Toki Pona through YouTube videos. What would you like to learn today?")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nAssistant: Goodbye! pona tawa sina!")
            break
        
        response = await chat_with_toki_pona_assistant(user_input, session)
        print(f"\nAssistant: {response}")

if __name__ == "__main__":
    asyncio.run(main())
