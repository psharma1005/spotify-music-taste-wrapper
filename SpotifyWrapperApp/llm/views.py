from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai import OpenAI
client = OpenAI()



prompt = f"""
You are a cultural analyst and writer for Spotify Wrapped. Based on the following music listening stats, write a fun and engaging personality profile:

- Genres listened to the most: {', '.join(genres)}
- Top artists: {', '.join(top_artists)}
- Total listening time: {listening_time} minutes
- Mood or theme of the music: {mood}

Create a playful and lighthearted description of how this person might think, act, or dress.
"""

query = ""
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": query
        }
    ]
)

print(completion.choices[0].message)
    

@api_view(['GET'])
def test_api(request):
    return Response({'message': 'Do you see this?'})






