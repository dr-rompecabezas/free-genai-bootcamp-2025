import re

from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    return match.group(1) if match else None


def download_vtt(youtube_url, output_file="captions.vtt"):
    """Fetch auto-generated subtitles from YouTube and save them as a VTT file."""
    video_id = get_video_id(youtube_url)
    if not video_id:
        print("Invalid YouTube URL.")
        return

    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Convert to VTT format
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for entry in transcript:
                start_time = entry["start"]
                text = entry["text"].replace(
                    "\n", " "
                )  # Ensure it's a single line per entry

                # Convert seconds to VTT timestamp format (hh:mm:ss.mmm)
                hours = int(start_time // 3600)
                minutes = int((start_time % 3600) // 60)
                seconds = start_time % 60

                timestamp = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
                f.write(f"{timestamp} --> {timestamp}\n{text}\n\n")

        print(f"VTT file saved as {output_file}")
    except Exception as e:
        print(f"Error fetching captions: {e}")


# Example Usage:
youtube_url = "https://www.youtube.com/watch?v=2EZihKCB9iw"
download_vtt(youtube_url)
