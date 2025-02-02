from flask import Flask, render_template, request, redirect, url_for
from youtube_transcript_api import YouTubeTranscriptApi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from urllib.parse import urlparse, parse_qs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path.startswith('/embed/'):
            return query.path.split('/')[2]
        if query.path.startswith('/v/'):
            return query.path.split('/')[2]
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def generate_summary(text, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return ' '.join([str(sentence) for sentence in summary])

def generate_mindmap(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    
    word_freq = Counter(filtered_words)
    top_words = [word for word, _ in word_freq.most_common(5)]
    
    mindmap = {"Main Topics": top_words}
    return mindmap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    video_url = request.form['url']
    video_id = extract_video_id(video_url)
    
    if not video_id:
        return redirect(url_for('index'))
    
    transcript = get_transcript(video_id)
    if not transcript:
        return render_template('error.html', message="Could not fetch transcript for this video")
    
    # Process transcript with timestamps
    transcript_with_timestamps = [
        {
            'time': f"{int(entry['start'] // 60):02d}:{int(entry['start'] % 60):02d}",
            'text': entry['text']
        } 
        for entry in transcript
    ]
    
    # Generate summary
    full_text = ' '.join([entry['text'] for entry in transcript])
    summary = generate_summary(full_text)
    
    # Generate mind map
    mindmap = generate_mindmap(full_text)
    
    return render_template('results.html',
                           transcript=transcript_with_timestamps,
                           summary=summary,
                           mindmap=mindmap)

if __name__ == '__main__':
    app.run(debug=True)