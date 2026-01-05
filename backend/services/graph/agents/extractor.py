from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from dotenv import load_dotenv
from ..utils import load_prompt

load_dotenv()

def optical_extractor(image_b64):
    """
        Extrair informações a partir de uma imagem
        Args:
            image_b64: Imagem no formato base64.
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": load_prompt("image_extractor")},
            {
                "type": "image",
                "base64": image_b64,
                "mime_type": "image/png",
            },
        ]
    )

    response = llm.invoke([message])

    return {
        'final_answer': response['messages'][-1].content,
    }

def audio_extractor(audio_b64):
    """
        Extrair informações a partir de um áudio
        Args:
            audio_b64: Áudio no formato base64.
    """
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": load_prompt("audio_extractor")},
            {
                "type": "audio",
                "base64": audio_b64,
                "mime_type": "audio/mpeg",
            },
        ]
    )

    response = llm.invoke([message])

    return {
        'final_answer': response['messages'][-1].content,
    }
