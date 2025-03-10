def search_youtube_videos(query):
    """
    Search YouTube for Toki Pona videos matching the query.
    
    Args:
        query (str): Search query related to Toki Pona
        
    Returns:
        list: List of dictionaries with video information:
            - id (str): YouTube video ID
            - title (str): Video title
            - channel (str): Channel name
            - duration (str): Video duration
            - description (str): Brief description
            - thumbnail_url (str): URL to video thumbnail
    """
    # YouTube API implementation
    # Uses YouTube Data API v3 to search for videos
    pass


def get_video_content(video_id):
    """
    Retrieve transcript and metadata for a YouTube video.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict:
            - transcript (str): Full transcript text
            - title (str): Video title
            - channel (str): Channel name
            - published_at (str): Publication date
            - has_subtitles (bool): Whether video had existing subtitles
            - language (str): Detected language of transcript
    """
    # Implementation using YouTube transcript API and metadata API
    # Falls back to speech-to-text if no subtitles available
    pass


class TokiPonaSession:
    def __init__(self):
        self.current_video_id = None
        self.current_content = None
        self.search_results = None
        self.suggestion_count = 0
        
    def get_state(self):
        """Return the current state for context inclusion"""
        return {
            "current_video_id": self.current_video_id,
            "has_video_content": self.current_content is not None,
            "suggestion_count": self.suggestion_count
        }
    

async def process_message(user_message, session):
    """Process a user message and return an agent response"""
    
    # Include relevant context from session state
    context = [
        {"role": "system", "content": "You are a Toki Pona learning assistant that helps students learn through YouTube videos. You can search for videos and retrieve their content to help students learn."},
        # Include session state in system message
    ]
    
    if session.current_video_id and session.current_content:
        # If we have a transcript, include it in context
        context.append({
            "role": "system", 
            "content": f"Current video: {session.current_content['title']} by {session.current_content['channel']}\n\nTranscript:\n{session.current_content['transcript']}"
        })
    
    context.append({"role": "user", "content": user_message})
    
    # Get model response with potential function calls
    response = await call_model(
        messages=context,
        functions={
            "search_youtube_videos": search_youtube_videos,
            "get_video_content": get_video_content
        }
    )
    
    # Handle function calls if any
    if hasattr(response, 'function_call') and response.function_call:
        # Execute the function
        function_name = response.function_call.name
        function_args = json.loads(response.function_call.arguments)
        
        if function_name == "search_youtube_videos":
            results = search_youtube_videos(**function_args)
            session.search_results = results
            session.suggestion_count += 1
            
        elif function_name == "get_video_content":
            content = get_video_content(**function_args)
            session.current_video_id = function_args.get("video_id")
            session.current_content = content
        
        # Get final response with function results
        final_context = context + [
            {"role": "assistant", "content": None, "function_call": response.function_call},
            {"role": "function", "name": function_name, "content": json.dumps(results if function_name == "search_youtube_videos" else content)}
        ]
        
        final_response = await call_model(messages=final_context)
        return final_response.content
    
    # If no function was called, return direct response
    return response.content
