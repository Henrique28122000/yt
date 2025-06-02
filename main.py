from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/extract")
def extract_video(request: VideoRequest):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'skip_download': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            formats = info.get('formats', [])
            links = [{'format_id': f['format_id'], 'ext': f['ext'], 'url': f['url']} for f in formats if f.get('url')]
            return {'title': info.get('title'), 'links': links}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
