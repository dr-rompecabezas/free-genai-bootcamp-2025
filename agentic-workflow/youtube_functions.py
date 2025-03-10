import os
import io
import tempfile
import requests
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from pytube import YouTube
import speech_recognition as sr
from pydub import AudioSegment

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
        dict: Transcript data including text and metadata
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
                "has_subtitles": True,
                "source": "youtube_api"
            }
        else:
            # No transcript available - return empty result
            return {
                "transcript": "",
                "language": "unknown",
                "is_generated": False,
                "has_subtitles": False,
                "source": "none"
            }
            
    except Exception as e:
        print(f"Error getting transcript: {str(e)}")
        return {
            "transcript": "",
            "language": "unknown",
            "is_generated": False,
            "has_subtitles": False,
            "source": "error",
            "error": str(e)
        }

def download_audio_from_youtube(video_id):
    """
    Download the audio from a YouTube video
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Path to temporary audio file or None if failed
    """
    try:
        # YouTube video URL
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Create a YouTube object
        yt = YouTube(url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            print("No audio stream found")
            return None
        
        # Create a temporary file for the audio
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"{video_id}.mp4")
        
        # Download the audio
        audio_stream.download(output_path=temp_dir, filename=f"{video_id}.mp4")
        
        return temp_file
    
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None

def generate_transcript_from_audio(audio_file_path, language="en-US"):
    """
    Generate transcript from audio file using speech recognition
    
    Args:
        audio_file_path (str): Path to the audio file
        language (str): Language code for speech recognition
        
    Returns:
        dict: Transcript data
    """
    try:
        # Check if file exists
        if not os.path.exists(audio_file_path):
            return {
                "transcript": "",
                "language": language,
                "is_generated": True,
                "has_subtitles": False,
                "source": "error",
                "error": "Audio file not found"
            }
        
        # Load audio file
        audio = AudioSegment.from_file(audio_file_path)
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Set up chunk size (30 seconds) for processing in parts
        chunk_length_ms = 30000  # 30 seconds
        chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        # Process each chunk
        full_transcript = ""
        for i, chunk in enumerate(chunks):
            print(f"Processing audio chunk {i+1}/{len(chunks)}...")
            
            # Export chunk to temporary WAV file
            chunk_file = os.path.join(tempfile.gettempdir(), f"chunk_{i}.wav")
            chunk.export(chunk_file, format="wav")
            
            # Process with speech recognition
            with sr.AudioFile(chunk_file) as source:
                audio_data = recognizer.record(source)
                try:
                    # Try to recognize speech
                    text = recognizer.recognize_google(audio_data, language=language)
                    full_transcript += text + " "
                except sr.UnknownValueError:
                    print(f"Chunk {i+1}: Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Chunk {i+1}: Could not request results; {e}")
            
            # Clean up temporary chunk file
            try:
                os.remove(chunk_file)
            except:
                pass
        
        if not full_transcript:
            return {
                "transcript": "Unable to generate transcript from audio.",
                "language": language,
                "is_generated": True,
                "has_subtitles": False,
                "source": "speech_recognition",
                "error": "No speech recognized"
            }
            
        # Return generated transcript
        return {
            "transcript": full_transcript.strip(),
            "language": language,
            "is_generated": True,
            "has_subtitles": False,
            "source": "speech_recognition"
        }
        
    except Exception as e:
        print(f"Error generating transcript: {str(e)}")
        return {
            "transcript": "",
            "language": language,
            "is_generated": True,
            "has_subtitles": False,
            "source": "error",
            "error": str(e)
        }
    finally:
        # Clean up the audio file if it exists
        try:
            if audio_file_path and os.path.exists(audio_file_path):
                os.remove(audio_file_path)
        except:
            pass

def get_transcript_from_anthropic(video_id, title, description):
    """
    As a fallback, use Anthropic's Claude to generate a transcript based on video metadata
    
    Args:
        video_id (str): YouTube video ID
        title (str): Video title
        description (str): Video description
        
    Returns:
        dict: Generated transcript data
    """
    try:
        from anthropic import Anthropic
        
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return {
                "transcript": "No Anthropic API key available for transcript generation.",
                "language": "en",
                "is_generated": True,
                "has_subtitles": False,
                "source": "error"
            }
        
        # Initialize client
        client = Anthropic(api_key=api_key)
        
        # Create prompt for video content inference
        system_prompt = """
        You are an expert in Toki Pona language. Based on the YouTube video title and description provided,
        generate a plausible transcript for what this video might contain. Focus on educational content
        about Toki Pona, including likely vocabulary, phrases, and explanations that would be taught.
        
        If the video appears to be a lesson, include:
        1. Common Toki Pona vocabulary with translations
        2. Basic sentence structures
        3. Example conversations
        4. Pronunciation guidance
        
        Make the transcript realistic, as if it were an actual transcription of a language learning video.
        Keep it concise but substantive, focusing on actual Toki Pona content.
        """
        
        # Call Claude to generate a plausible transcript
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Using smaller model for speed
            max_tokens=1500,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"""
                Generate a plausible transcript for this Toki Pona learning video:
                
                Video ID: {video_id}
                Title: {title}
                Description: {description}
                
                Generate only the transcript content, not any explanation or framing.
                """}
            ]
        )
        
        # Extract the text response
        response_text = None
        if hasattr(response, 'content') and response.content:
            for content_item in response.content:
                if content_item.type == "text":
                    response_text = content_item.text
        
        if not response_text:
            return {
                "transcript": "Failed to generate transcript.",
                "language": "en",
                "is_generated": True,
                "has_subtitles": False,
                "source": "error"
            }
            
        return {
            "transcript": response_text.strip(),
            "language": "en",
            "is_generated": True,
            "has_subtitles": False,
            "source": "anthropic"
        }
            
    except Exception as e:
        print(f"Error generating transcript with Anthropic: {str(e)}")
        return {
            "transcript": "Error generating transcript.",
            "language": "en",
            "is_generated": True,
            "has_subtitles": False,
            "source": "error",
            "error": str(e)
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
        
        # Get transcript data using the YouTube API
        transcript_data = get_video_transcript(video_id)
        
        # If no transcript is available, try to generate one from audio
        if not transcript_data["transcript"]:
            print(f"No transcript available for video {video_id}. Attempting to generate from audio...")
            
            # Try speech recognition approach first
            audio_file_path = download_audio_from_youtube(video_id)
            if audio_file_path:
                # Determine language for speech recognition
                # Default to English, but use video language if available
                language_code = snippet.get("defaultAudioLanguage", "en-US")
                
                # Convert YouTube language codes to speech recognition format if needed
                if language_code == "tok":
                    language_code = "en-US"  # Default to English for Toki Pona
                elif len(language_code) == 2:
                    language_code = f"{language_code}-{language_code.upper()}"
                
                # Generate transcript from audio
                transcript_data = generate_transcript_from_audio(audio_file_path, language_code)
            
            # If speech recognition failed or produced empty results, try Anthropic as fallback
            if not transcript_data["transcript"] or transcript_data.get("error"):
                print("Speech recognition failed or empty. Using Anthropic to generate transcript...")
                transcript_data = get_transcript_from_anthropic(
                    video_id,
                    snippet["title"],
                    snippet["description"]
                )
        
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
            "transcript": transcript_data["transcript"],
            "transcript_source": transcript_data["source"],
            "is_generated_transcript": transcript_data["is_generated"]
        }
        
        return video_content
        
    except Exception as e:
        print(f"Error getting video content: {str(e)}")
        return {
            "error": f"Error retrieving video content: {str(e)}"
        }
