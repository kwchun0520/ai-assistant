## to be implemented: load_uploaded_document_tool

from pathlib import Path
from typing import Any, Dict

from google import genai
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai.types import GenerateContentConfig, Modality
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_core.documents import Document
from loguru import logger

from ai_assistant.utils import load_yaml

# Load prompt configuration from the YAML file
prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)


async def load_weblink(url: str, tool_context: ToolContext) -> Dict[str, Any]:
    """ Loads a web page and returns its content.

    Args:
        url (str): The URL of the web page to load.

    Returns:
        Dict[str, Any]: A dictionary containing the loaded document object (Langchain Document Object).
    """
    loader = WebBaseLoader(url)
    document = loader.load()[0]
    tool_context.state["temp:document"] = document.page_content
    return {"document": document}

def load_text(text: str, tool_context: ToolContext) -> Dict[str, Any]:
    """ Loads a text and returns it as a document.

    Args:
        text (str): The text to load.

    Returns:
        Dict[str, Any]: A dictionary containing the loaded document object (Langchain Document Object).
    """
    document = Document(page_content=text, metadata={})
    tool_context.state["temp:document"] = document
    return {"document": document}


###  to be implemented

def save_uploaded_document(tool_context: ToolContext) -> None:
    """ Saves an uploaded document to the tool context state.

    Args:
        file_path (str): The path to the uploaded document.
        tool_context (ToolContext): The context in which the tool is executed.
    """
    

def load_uploaded_document(tool_context:ToolContext) -> Dict[str, Any]: 
    """ Loads an uploaded file and returns its content.

    Args:
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        Dict[str, Any]: A dictionary containing the loaded document object (Langchain Document Object).
    """
    if tool_context.user_content and tool_context.user_content.parts:
        logger.info(tool_context.user_content.parts)
    logger.info("Loading uploaded document...")
    
    loader = PyPDFLoader(tool_context.state["temp:document_path"])
    document = loader.load()
    tool_context.state["temp:document"].append(document)
    return {"document": document}
    
###  to be implemented
    

    
async def summarize_document(tool_context: ToolContext) -> Dict[str, Any]:
    """ Summarizes a web page and saves the summary in the tool context.

    Args:
        url (str): The URL of the web page to summarize.
        tool_context (ToolContext): The context in which the tool is executed.

    Returns:
        Dict[str, Any]: A dictionary containing the summary.
    """
    
    
    document = tool_context.state.get("temp:document")
    if not document:
        logger.error("No document found in tool context state.")
        return {"error": "No document found in tool context state."}

    # tool_context.state["temp:document"] = document
    
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=CONFIG["summarization_prompt"] + document,
        config=GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_modalities=[Modality.TEXT],
        ),
    )
    return response
    
    
    
load_weblink_tool = FunctionTool(func=load_weblink)
load_text_tool = FunctionTool(func=load_text)
# load_uploaded_document_tool = FunctionTool(func=load_uploaded_document)
summarize_document_tool = FunctionTool(func=summarize_document)