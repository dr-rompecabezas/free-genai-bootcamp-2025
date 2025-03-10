import os
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime

def setup_youtube_api():
    """Initialize the YouTube API client"""
    api_service_name = "youtube"
    api_version = "v3"
    youtube_api_key = os.environ.get("YOUTUBE_API_KEY")
    
    if not youtube_api_key:
        raise ValueError("YouTube API key not found. Please set the YOUTUBE_API_KEY environment variable.")
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=youtube_api_key
    )
    
    return youtube

def search_youtube_videos(query):
    """
    Search YouTube for videos matching the query
    
    Args:
        query (str): Search query related to Toki Pona
        
    Returns:
        list: List of video information dictionaries
    """
    youtube = setup_youtube_api()
    
    # Add "toki pona" to the query if not already present to focus results
    if "toki pona" not in query.lower():
        query = f"toki pona {query}"
    
    # Call the search.list method to retrieve results
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=5,
        type="video",
        relevanceLanguage="en",  # Prefer English results but will include others
    ).execute()
    
    # Format results for the assistant
    results = []
    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        
        # Get additional video details like duration
        video_details = youtube.videos().list(
            part="contentDetails,statistics",
            id=video_id
        ).execute()
        
        if video_details["items"]:
            details = video_details["items"][0]
            duration_iso = details["contentDetails"]["duration"]  # ISO 8601 format
            # Convert ISO 8601 duration to simple minutes:seconds format
            # For simplicity, only handling typical lesson video durations (< 1 hour)
            duration = duration_iso.replace("PT", "")
            minutes = 0
            seconds = 0
            if "M" in duration:
                minutes_part = duration.split("M")[0]
                minutes = int(minutes_part)
                duration = duration.split("M")[1]
            if "S" in duration:
                seconds_part = duration.split("S")[0]
                seconds = int(seconds_part)
            
            formatted_duration = f"{minutes}:{seconds:02d}"
            view_count = details["statistics"].get("viewCount", "0")
        else:
            formatted_duration = "Unknown"
            view_count = "Unknown"
            
        # Format the result
        results.append({
            "id": video_id,
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "duration": formatted_duration,
            "description": item["snippet"]["description"],
            "published_at": item["snippet"]["publishedAt"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "view_count": view_count
        })
    
    return results

def get_video_transcript(video_id):
    """
    Get transcript for a specific video
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Formatted transcript text or error message
    """
    try:
        # Attempt to get transcript in any available language
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # First try to find English or Toki Pona transcripts
        preferred_transcript = None
        for transcript in transcript_list:
            if transcript.language_code in ['en', 'tok']:  # 'tok' is language code for Toki Pona
                preferred_transcript = transcript
                break
        
        # If no preferred language found, use the first available transcript
        if not preferred_transcript and transcript_list:
            preferred_transcript = transcript_list[0]
        
        if preferred_transcript:
            transcript_data = preferred_transcript.fetch()
            
            # Format the transcript as text
            formatted_transcript = ""
            for entry in transcript_data:
                formatted_transcript += f"{entry['text']} "
            
            return {
                "transcript": formatted_transcript.strip(),
                "language": preferred_transcript.language_code,
                "is_generated": preferred_transcript.is_generated,
                "has_subtitles": True
            }
        else:
            return {
                "transcript": "No transcript available for this video.",
                "language": "unknown",
                "is_generated": False,
                "has_subtitles": False
            }
            
    except Exception as e:
        print(f"Error getting transcript: {str(e)}")
        return {
            "transcript": f"Error retrieving transcript: {str(e)}",
            "language": "unknown",
            "is_generated": False,
            "has_subtitles": False
        }

def get_video_content(video_id):
    """
    Get comprehensive details about a video including its transcript
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Video metadata and transcript
    """
    youtube = setup_youtube_api()
    
    try:
        # Get video details
        video_response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        ).execute()
        
        if not video_response["items"]:
            return {
                "error": f"Video with ID {video_id} not found"
            }
        
        video_data = video_response["items"][0]
        snippet = video_data["snippet"]
        
        # Get transcript data
        transcript_data = get_video_transcript(video_id)
        
        # Format the response
        video_content = {
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "description": snippet["description"],
            "published_at": snippet["publishedAt"],
            "view_count": video_data["statistics"].get("viewCount", "0"),
            "like_count": video_data["statistics"].get("likeCount", "0"),
            "comment_count": video_data["statistics"].get("commentCount", "0"),
            "has_subtitles": transcript_data["has_subtitles"],
            "transcript_language": transcript_data["language"],
            "transcript": transcript_data["transcript"]
        }
        
        return video_content
        
    except Exception as e:
        print(f"Error getting video content: {str(e)}")
        return {
            "error": f"Error retrieving video content: {str(e)}"
        }
