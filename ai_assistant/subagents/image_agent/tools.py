import base64
import os
import uuid
from pathlib import Path
from typing import Any, Dict

from google import genai
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai.types import (Blob, GenerateContentConfig,
                                GenerateImagesConfig, Modality, Part)
from loguru import logger

from ai_assistant.utils import load_yaml

# Load prompt configuration from the YAML file
prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)

EXAMPLE_PROMPT = CONFIG['example_prompt']

async def _save_image(data: bytes, mime_type:str, tool_context:ToolContext) -> Dict[str, Any]:
    """Saves the image data to a file and returns the file path.

    Args:
        data (bytes): The image data to save.

    Returns:
        Dict[str, Any]: A dictionary containing the filename, artifact version, and a confirmation message.
    """
    local_folder_path = "images"
    os.makedirs(local_folder_path, exist_ok=True) 
    
    extension = mime_type.split("/")[-1]
    filename = f"image_{uuid.uuid4()}.{extension}" 
    with open(f"{local_folder_path}/{filename}", "wb") as f:
        f.write(data)
    
    local_file_path = f"{local_folder_path}/{filename}"
    artifact_part = Part(inline_data=Blob(data=data, mime_type=mime_type))
    
    artifact_object = await tool_context.save_artifact(
        filename=filename,
        artifact=artifact_part,
    )
    logger.info(f"Image saved to local path: {local_file_path}")
    confirmation_msg = f"Image artifact {filename} saved. Image saved on local at {local_file_path}"
    
    tool_context.state["image_artifact"] = {
        "filename": filename,
        "artifact_version": artifact_object,
        "image_bytes": base64.b64encode(data),
    }
    
    return {
        "filename": filename,
        "artifact_version": artifact_object,
        "confirmation": confirmation_msg
    }
    
# image_save_tool = FunctionTool(func=_save_image)


async def generate_image(prompt: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Generates an image based on a text prompt using Gemini API.

    Args:
        prompt (str): The text description for the image to be generated.
        tool_context (ToolContext): The context for the tool, which includes methods to save artifacts.
    Returns:
        Dict[str, Any]: A dictionary containing information about the generated image, including
                        the artifact name and version where the image is stored.
    """

    client = genai.Client()
    data = None
    artifact = None
    try:
        response = client.models.generate_images(
        model=CONFIG['image_model'],
        prompt = prompt,
        config=GenerateImagesConfig(
            number_of_images=1
        ))
        data = response.generated_images[0].image.image_bytes
        mime_type = response.generated_images[0].image.mime_type
            # data = image.image_bytes
            # mime_type = image.mime_type
        artifact = await _save_image(data=data, mime_type=mime_type, tool_context=tool_context)
            
        return artifact
    
    except Exception as e:
        return {"error":str(e)}
    
    
async def enhance_prompt(desc: str, tool_context: ToolContext) -> dict:
    """
    Enhances a text prompt using Gemini API.

    Args:
        prompt (str): The text description to be enhanced.

    Returns:
       dict: A dictionary containing the user description of the image and the enhanced prompt.
    """
    
    client = genai.Client()

    input_prompt = f"""
        You are a creative image generation assistant that enhances text prompts.
        Enhance the following text prompt to make it more descriptive and suitable for image generation:
        "{desc}"
        
        Examples: 
        - {EXAMPLE_PROMPT}
        
        Return the enhanced prompt only as a single string.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=input_prompt,
        config=GenerateContentConfig(
            temperature=0.5,
            response_modalities=[Modality.TEXT],
        ),
    )
    
    return {"user_description": desc, "enhanced_prompt": response.candidates[0].content.parts[0].text}


generate_image_tool = FunctionTool(func=generate_image)
enhance_prompt_tool = FunctionTool(func=enhance_prompt)
