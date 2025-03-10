import os
import json
import asyncio
from anthropic import Anthropic
from dotenv import load_dotenv
from youtube_functions import search_youtube_videos, get_video_content

# Load environment variables
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
    },
    {
        "name": "extract_vocabulary",
        "description": "Extracts Toki Pona vocabulary from a transcript with definitions. Use this to help students learn vocabulary from a video.",
        "input_schema": {
            "type": "object",
            "properties": {
                "transcript": {
                    "type": "string",
                    "description": "The transcript text from which to extract Toki Pona vocabulary"
                }
            },
            "required": ["transcript"]
        }
    },
    {
        "name": "generate_quiz",
        "description": "Creates a quiz based on the current video's content. Use this when the student wants to test their knowledge.",
        "input_schema": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "string", 
                    "enum": ["beginner", "intermediate", "advanced"],
                    "description": "The difficulty level of the quiz",
                    "default": "beginner"
                },
                "question_count": {
                    "type": "integer",
                    "description": "Number of questions to generate",
                    "default": 5
                }
            },
            "required": []
        }
    }
]

# Implementation of the natural language processing tools
def extract_vocabulary(transcript):
    """
    Extract Toki Pona vocabulary from a transcript
    This is a more sophisticated implementation that would be better handled by Claude
    but we include it as a separate function for modularity
    """
    # Since this requires language understanding, we'll use Claude for this task
    system_prompt = """
    You are a Toki Pona language expert. Extract all Toki Pona words from the given transcript.
    For each word:
    1. Provide the Toki Pona word
    2. Provide its English definition
    3. Include an example sentence from the transcript if available
    
    Format the response as a JSON array of objects with keys: "word", "definition", "example"
    """
    
    try:
        # Call Claude to extract vocabulary
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",  # Using a smaller model for quick analysis
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"Extract Toki Pona vocabulary from this transcript:\n\n{transcript}"}
            ]
        )
        
        # Extract the text response
        response_text = None
        if hasattr(response, 'content') and response.content:
            for content_item in response.content:
                if content_item.type == "text":
                    response_text = content_item.text
        
        if not response_text:
            return {"vocabulary": [], "error": "Failed to extract vocabulary"}
        
        # Try to parse JSON from the response
        try:
            # Find JSON in the response - it may be wrapped in markdown code blocks
            if "```json" in response_text:
                json_part = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_part = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_part = response_text
                
            vocabulary = json.loads(json_part)
            return {"vocabulary": vocabulary}
        except json.JSONDecodeError:
            # If parsing fails, return the raw text
            return {
                "vocabulary": [],
                "error": "Failed to parse vocabulary as JSON",
                "raw_response": response_text
            }
            
    except Exception as e:
        print(f"Error extracting vocabulary: {str(e)}")
        return {"vocabulary": [], "error": str(e)}

def generate_quiz(difficulty="beginner", question_count=5, transcript=None, video_title=None):
    """
    Generate a quiz based on video content
    This is handled by Claude due to its language understanding capabilities
    """
    if not transcript:
        return {"error": "No transcript available for quiz generation"}
    
    system_prompt = f"""
    You are a Toki Pona language teacher. Create a {difficulty} level quiz with {question_count} questions 
    based on the provided transcript from the video "{video_title}".
    
    For beginner quizzes, focus on:
    - Simple vocabulary recognition
    - Basic sentence structure
    - Matching Toki Pona words to English meanings
    
    For intermediate quizzes, include:
    - Sentence translation (both directions)
    - Fill-in-the-blank exercises
    - Understanding context
    
    For advanced quizzes, include:
    - Complex sentence translation
    - Idioms and expressions
    - Creating original Toki Pona sentences
    
    Format the response as a JSON object with:
    1. "title": Quiz title
    2. "difficulty": The difficulty level
    3. "questions": Array of question objects, each with:
       - "question": The question text
       - "options": Array of possible answers (for multiple choice)
       - "correct_answer": The correct answer
       - "explanation": Brief explanation of the answer
    
    Use the transcript content to create relevant questions.
    """
    
    try:
        # Call Claude to generate the quiz
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",  # Using a mid-size model for quality
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"Generate a {difficulty} level Toki Pona quiz based on this transcript:\n\n{transcript}"}
            ]
        )
        
        # Extract the text response
        response_text = None
        if hasattr(response, 'content') and response.content:
            for content_item in response.content:
                if content_item.type == "text":
                    response_text = content_item.text
        
        if not response_text:
            return {"error": "Failed to generate quiz"}
        
        # Try to parse JSON from the response
        try:
            # Find JSON in the response - it may be wrapped in markdown code blocks
            if "```json" in response_text:
                json_part = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_part = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_part = response_text
                
            quiz = json.loads(json_part)
            return quiz
        except json.JSONDecodeError:
            # If parsing fails, return the raw text
            return {
                "error": "Failed to parse quiz as JSON",
                "raw_response": response_text
            }
            
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return {"error": str(e)}

# Function registry with the actual implementations
function_registry = {
    "search_youtube_videos": search_youtube_videos,
    "get_video_content": get_video_content,
    "extract_vocabulary": extract_vocabulary,
    "generate_quiz": generate_quiz
}

class TokiPonaSession:
    def __init__(self):
        self.search_results = None
        self.current_video_id = None
        self.current_content = None
        self.vocabulary = None
        self.quiz = None
        self.conversation_history = []
        self.suggested_videos = 0  # Track number of videos suggested
        self.max_suggestions = 3   # Maximum number of video suggestions before defaulting
    
    def add_user_message(self, content):
        self.conversation_history.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        self.conversation_history.append({"role": "assistant", "content": content})
    
    def reset_suggestions(self):
        self.suggested_videos = 0
    
    def increment_suggestions(self):
        self.suggested_videos += 1
    
    def suggestions_exceeded(self):
        return self.suggested_videos >= self.max_suggestions

async def chat_with_toki_pona_assistant(user_message, session):
    """Process a user message with the Toki Pona assistant"""
    
    # Add the user message to the conversation history
    session.add_user_message(user_message)
    
    # Include current context in system prompt
    context = """You are a helpful Toki Pona learning assistant that guides students through learning Toki Pona using YouTube videos.

When presenting video search results to the student:
1. Include the full YouTube URL for each video
2. Format results in a numbered list for easy selection
3. Include title, channel, duration, and view count

When a student selects a video, always provide them with the direct link to watch it on YouTube.
"""
    
    # Add search results context if available
    if session.search_results and len(session.search_results) > 0:
        context += "\n\nRecent search results:"
        for i, video in enumerate(session.search_results[:3], 1):
            context += f"\n{i}. {video.get('title')} by {video.get('channel')} ({video.get('duration')}) - {video.get('url')}"
    
    # Add video context if available
    if session.current_content:
        video_url = session.current_content.get('url', '')
        video_context = f"\nCurrent video: {session.current_content.get('title', 'Unknown')} by {session.current_content.get('channel', 'Unknown')}"
        
        if video_url:
            video_context += f"\nVideo URL: {video_url}"
        
        # Add transcript source information
        if session.current_content.get('is_generated_transcript', False):
            source = session.current_content.get('transcript_source', 'unknown')
            if source == 'speech_recognition':
                video_context += "\n[Transcript was automatically generated from audio using speech recognition]"
            elif source == 'anthropic':
                video_context += "\n[Transcript was generated based on video title and description]"
            else:
                video_context += "\n[Transcript was automatically generated]"
        
        # Only include transcript if it's not too long
        transcript = session.current_content.get('transcript', '')
        if len(transcript) > 1000:
            # Truncate for context but keep full version for tools
            transcript_summary = transcript[:1000] + "... [transcript continues]"
            context += f"{video_context}\n\nTranscript excerpt: {transcript_summary}"
        else:
            context += f"{video_context}\n\nTranscript: {transcript}"
    
    # Add vocabulary context if available
    if session.vocabulary:
        vocab_count = len(session.vocabulary.get('vocabulary', []))
        context += f"\n\nExtracted vocabulary: {vocab_count} words available from current video."
    
    # Add quiz context if available
    if session.quiz:
        context += f"\n\nCurrent quiz: {session.quiz.get('title', 'Quiz')} ({session.quiz.get('difficulty', 'beginner')} difficulty) with {len(session.quiz.get('questions', []))} questions."
    
    # Include the suggestion limit process
    context += f"\n\nFollow the Toki Pona learning workflow. After {session.max_suggestions} video suggestions without acceptance, default to recommending a pre-selected option."
    
    # Call Claude with tools
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2048,
        system=context,
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
                
                # Special handling for certain tools
                if function_name == "extract_vocabulary" and session.current_content:
                    # Use current video transcript if not provided
                    if "transcript" not in function_args and session.current_content.get("transcript"):
                        function_args["transcript"] = session.current_content["transcript"]
                
                if function_name == "generate_quiz" and session.current_content:
                    # Use current video transcript if not provided
                    if "transcript" not in function_args and session.current_content.get("transcript"):
                        function_args["transcript"] = session.current_content["transcript"]
                        function_args["video_title"] = session.current_content.get("title", "Toki Pona Video")
                
                # Call the appropriate function if in registry
                if function_name in function_registry:
                    function_result = function_registry[function_name](**function_args)
                    
                    # Update session based on function call
                    if function_name == "search_youtube_videos":
                        session.search_results = function_result
                        session.increment_suggestions()
                    elif function_name == "get_video_content":
                        session.current_video_id = function_args.get("video_id")
                        session.current_content = function_result
                        session.reset_suggestions()  # Reset suggestion count when video selected
                    elif function_name == "extract_vocabulary":
                        session.vocabulary = function_result
                    elif function_name == "generate_quiz":
                        session.quiz = function_result
                    
                    # Store assistant's tool use message
                    session.add_assistant_message([
                        {"type": "tool_use", "id": tool_use.id, "name": tool_use.name, "input": tool_use.input}
                    ])
                    
                    # Store user's tool result message
                    session.add_user_message([
                        {"type": "tool_result", "tool_use_id": tool_use.id, "content": json.dumps(function_result)}
                    ])
                    
                    # Get final response with function results
                    final_response = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=2048,
                        system=context,
                        messages=session.conversation_history[-12:]  # Include recent tool calls
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
    session = TokiPonaSession()
    
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
