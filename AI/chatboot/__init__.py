import os
import uuid
from dotenv import load_dotenv
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
import re

load_dotenv("env/chatbot.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
PROJECT_NAME = os.getenv("PROJECT_NAME")

def get_random_quote(language:str ) -> str:
    """
    Fetches a random quote about respecting the coastline and picking up litter using Gemini API.

    Returns:
        str: A random quote.
    """
    try:
        # Utilisation du modèle Gemini pour générer une citation
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, google_api_key=GEMINI_API_KEY, project=PROJECT_NAME
        )
        

        # Prompt pour générer une citation sur le respect du littoral et le ramassage des poubelles
        prompt = "**Je suis Bard, un modèle de langage conçu pour vous fournir dans 1 ligne just des petites citations inspirantes sur le respect du littoral et l'importance de ramasser les poubelles. Voici votre citation en anglais :**"
        result = llm.invoke(prompt)
        quote = result.content.strip()
        if language == "francais":
            prompt = f"**je suis un expert en traduction, je peux traduire cette citation en français voila la citation en anglais:{quote}. Voici votre citation en français :**"
            result = llm.invoke(prompt)
            quote = result.content.strip()
        elif language == "arabe":
            prompt = f"**je suis un expert en traduction, je peux traduire cette citation en arabe voila la citation en anglais:{quote}. Voici votre citation en arabe :**"
            result = llm.invoke(prompt)
            quote = result.content.strip()

        else:
            quote = quote

        return quote    

    except Exception as e:
        return f"An error occurred while fetching the quote: {e}"

def get_recyclage_idea(question: str) -> str:
    # Specify the Gemini model and API key
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME, google_api_key=GEMINI_API_KEY, project=PROJECT_NAME
    )

    # Craft the prompt template for Gemini
    prompt = f"**Je suis Bard, un modèle de langage conçu pour vous aider avec des idées de recyclage facile. Demandez-moi n'importe quoi et je vais repondre a touts vos questions concernant le recyclage , si c'est pas le cas je vais pas repondre   !**\nVoici la question de l'utilisateur : {question}"

    # Call Gemini to generate the answer
    result = llm.invoke(prompt)

    # Extract the answer from the response (assuming it's the first sentence)
    answer = result.content.strip()
    print(answer)

    return answer