from dotenv import load_dotenv
import os
from openai import OpenAI


class OpenAIClass:

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        org_id = os.getenv("OPENAI_ORG_ID")
        client = OpenAI(api_key=api_key, organization=org_id)
        self.client = client

    def get_embedding_from_text(self, text):
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-ada-002",
        )
        return response.data[0].embedding

    def get_chat_response_from_openai(self, prompt):
        messages = [
            {"role": "system", "content": "You are an expert in creating TV shows. When given the names and the "
                                          "descriptions of multiple TV shows, your goal is to create a new TV show that is "
                                          "similar to them."
                                          "you have to provide a title and a description of the new TV show."},
            {"role": "user",
             "content": f"These are the TV shows and their descriptions: {prompt}. Answer in the following"
                        f"format: <title>, description: <description>"},
        ]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        return response.choices[0].message.content

    def get_image_from_dalle(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url
