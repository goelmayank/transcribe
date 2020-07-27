from flask import Flask, request, render_template
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup as bs
import re

app = Flask(__name__)

def transcribe(video_id):
    try:
    # retrieve the available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # iterate over all available transcripts
        for transcript in transcript_list:
            transcript = transcript.fetch()
            subtitles = ""
            for subtitle in transcript:
                subtitles+=(subtitle['text']+' ')

            r = requests.post('http://bark.phon.ioc.ee/punctuator', data={'text':subtitles})
            r2 = requests.get("https://www.youtube.com/watch?v="+video_id)
            soup = bs(r2.content)
            title = soup.find("meta", {"name": "title"})['content']
            cleanString = re.sub('\W+',' ', title )
            # writeToFile("./subtitles.txt", r.text)
            d = dict()
            d['subtitle'] = r.text+"<h4>URL: https://www.youtube.com/watch?v="+video_id+"  </h4><iframe width='420' height='345' src='https://www.youtube.com/embed/"+video_id+"'></iframe>"
            d['title']   = cleanString
            return d
    except:
        err = dict()
        err['subtitle'] = "<h4>URL: https://www.youtube.com/watch?v="+video_id+"  </h4><iframe width='420' height='345' src='https://www.youtube.com/embed/"+video_id+"'></iframe>"
        err['title']   = "Subtitle doesn't found for video"
        return err


@app.route('/getsubtitle')
def root():
    video_id = request.args.get('video_id', default="iN1s3jvT_OU", type=str)
    subtitles = transcribe(str(video_id))
    return "<h2>"+subtitles['title']+"</h2>"+"<p>"+subtitles['subtitle']+"</p>"
    return render_template('index.html', times=subtitles)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
