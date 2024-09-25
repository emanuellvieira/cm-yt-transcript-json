from flask import Flask, render_template, request, send_file
from youtube_transcript_api import YouTubeTranscriptApi
import json
import re
import os

app = Flask(__name__)

# Função para extrair o ID do vídeo da URL
def extract_video_id(url):
    video_id_match = re.search(r"(v=|/v/|youtu\.be/|/live/|embed/|/watch\?v=)([a-zA-Z0-9_-]{11})", url)
    if video_id_match:
        return video_id_match.group(2)
    return None

# Função para extrair a transcrição do YouTube
def get_transcription(video_id, language='pt'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return transcript
    except Exception as e:
        print(f"Erro ao obter a transcrição: {e}")
        return None

# Rota principal para a página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        video_id = extract_video_id(video_url)
        
        if video_id:
            transcript = get_transcription(video_id)
            if transcript:
                output_file = f"transcription_{video_id}.json"
                with open(output_file, 'w', encoding='utf-8') as json_file:
                    json.dump(transcript, json_file, ensure_ascii=False, indent=4)
                
                return send_file(output_file, as_attachment=True)
            else:
                return "Nenhuma transcrição encontrada para o vídeo."
        else:
            return "URL inválida. Verifique a URL do vídeo."
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
