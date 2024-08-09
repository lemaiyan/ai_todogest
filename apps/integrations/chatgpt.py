import openai
import re
import time
from django.conf import settings
from structlog import get_logger

logger = get_logger()


class Preprocess:
    def __init__(self):
        logger.info("Initializing AI Model")
        self.model = settings.CHAGPT_MODEL
        self.key = settings.CHAGPT_KEY
        openai.api_key = self.key

    def prompt(self, text, type="gmail"):
        logger.info("Prompting AI Model")
        system_prompt = '''You are a language model that gives content based on a prompt.'''
        prompt = f'''I need help getting started with a task on my to-do list. 
                Can you provide me with a brief overview and some starter 
                content for the following task: {text}? 
                Please include the key steps involved, any important considerations, 
                and useful tips to help me complete this task efficiently.'''
        style = "give the the response in formatted in html only but remove the html tags"
        if type == "outlook":
            style = "give the the response in formatted in html only but remove the html tags"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": style},
            {"role": "assistant", "content": "On what topic?"},
            {"role": "user", "content": prompt}
        ]
        responses = openai.ChatCompletion.create(model=self.model, messages=messages)
        content = responses.choices[0].message["content"]
        logger.info("AI Model response", response=content)
        return content


class EmailSummary:
    def __init__(self):
        logger.info("Initializing AI Model for Email Summarization")
        self.model = settings.CHAGPT_MODEL
        self.key = settings.CHAGPT_KEY
        openai.api_key = self.key

    def __chunk_text(self, email_body, max_chars=3000):
        paragraphs = re.split(r'\n+', email_body)
        chunks = []
        current_chunk = ''

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chars:
                current_chunk += paragraph + '\n'
            else:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def summarize_email(self, email_body):
        text_chunks = self.__chunk_text(email_body, 3000)  # Use a smaller character limit to accommodate token limits
        summarized_chunks = []
        for idx, email_text in enumerate(text_chunks):
            if idx >= 5:
                # Limit to 5 chunks
                break
            if len(email_text) > 0:
                logger.info("email summarization")
                system_prompt = '''You are a language model that summarizes emails in 3-5 bullet points.'''
                user_input = f'''Please summarize the following email into 3-5 concise bullet points, highlighting the main points and key information: {email_text}'''
                style = "Powerpoint slide with 3-5 bullet points with </br> at the end of each bullet point"
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": style},
                    {"role": "assistant", "content": "On what topic?"},
                    {"role": "user", "content": user_input}
                ]
                max_retries = 3
                retry_count = 0
                retry_flag = True

                while retry_flag and retry_count < max_retries:
                    try:
                        logger.info("calling openai api to summarize email")
                        response = openai.ChatCompletion.create(
                            model=settings.CHAGPT_MODEL,
                            messages=messages,
                            temperature=1,
                            top_p=1,
                            presence_penalty=0.5,
                            frequency_penalty=0.4
                        )
                        logger.info("openai api response", response=response)
                        # Extract the generated text from the API response
                        email_summary_chunk = (response['choices'][0]['message']['content'])
                        summarized_chunks.append(email_summary_chunk)
                        retry_flag = False
                    except Exception:
                        logger.exception("openai api call failed")
                        retry_count += 1
                        time.sleep(3)

            email_summary = ' '.join(summarized_chunks)

            return email_summary
