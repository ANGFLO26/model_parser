import requests
from dots_ocr.utils.image_utils import PILimage_to_base64

from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio
import time
import random

load_dotenv()

async def async_inference_with_api(
        image,
        prompt, 
        base_url=None,
        api_key=None,
        protocol="http",
        ip="localhost",
        port=8000,
        temperature=0.1,
        top_p=0.9,
        max_completion_tokens=32768,
        model_name='rednote-hilab/dots.ocr',
        request_delay=2.0,
        ):
    
    # Initial delay to throttle requests
    if request_delay > 0:
        await asyncio.sleep(request_delay)

    # Determine provider based on model name
    is_openai_model = "gpt" in model_name.lower()
    is_gemini_model = "gemini" in model_name.lower()

    if is_openai_model:
        # OpenAI specific configuration
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        final_api_key = os.environ.get("OPENAI_API_KEY")
        if not final_api_key:
             print("WARNING: OPENAI_API_KEY not found in environment variables.")
    else:
        # Existing logic for Gemini/Local/Other
        if base_url is None:
            # Check if BASE_URL is in env
            env_base_url = os.environ.get("BASE_URL")
            if env_base_url:
                base_url = env_base_url
            else:
                base_url = f"{protocol}://{ip}:{port}/v1"
        
        # Priority: Argument > API_KEY env > GOOGLE_API_KEY env > "EMPTY"
        final_api_key = api_key or os.environ.get("API_KEY") or os.environ.get("GOOGLE_API_KEY") or "EMPTY"
    
    # Default model from env if not provided or stuck on default (Only for Gemini scenarios usually)
    if model_name == 'rednote-hilab/dots.ocr' and os.environ.get("GEMINI_MODEL"):
         model_name = os.environ.get("GEMINI_MODEL")

    client = AsyncOpenAI(api_key=final_api_key, base_url=base_url)
    
    # Prompt adjustment
    # Both Gemini via OpenAI connector and Native OpenAI GPT should use plain text prompt
    if is_gemini_model or is_openai_model:
        text_content = prompt
    else:
        text_content = f"<|img|><|imgpad|><|endofimg|>{prompt}"

    messages = []
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url":  PILimage_to_base64(image)},
                },
                {"type": "text", "text": text_content} 
            ],
        }
    )
    
    max_retries = 8
    base_delay = 5 # seconds

    try:
        for attempt in range(max_retries):
            try:
                response = await client.chat.completions.create(
                    messages=messages, 
                    model=model_name, 
                    max_completion_tokens=max_completion_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
                break # Success
            except Exception as e:
                # Check for rate limit error (usually 429)
                if "429" in str(e) or "quota" in str(e).lower():
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                        delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                        print(f"Rate limited (429). Retrying in {delay:.2f}s...")
                        await asyncio.sleep(delay)
                        continue
                raise e # Re-raise other errors or if retries exhausted

        response_content = response.choices[0].message.content
        
        # Clean up markdown formatting if present (common with Gemini)
        if response_content.startswith("```json"):
            response_content = response_content[7:]
        elif response_content.startswith("```"):
            response_content = response_content[3:]
        
        if response_content.endswith("```"):
            response_content = response_content[:-3]
            
        return response_content.strip()
    except requests.exceptions.RequestException as e:
        print(f"request error: {e}")
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None

def inference_with_api(
        image,
        prompt, 
        base_url=None,
        api_key=None,
        protocol="http",
        ip="localhost",
        port=8000,
        temperature=0.1,
        top_p=0.9,
        max_completion_tokens=32768,
        model_name='rednote-hilab/dots.ocr',
        request_delay=2.0,
        ):
    
    # Initial delay to throttle requests
    if request_delay > 0:
        time.sleep(request_delay)

    # Determine provider based on model name
    is_openai_model = "gpt" in model_name.lower()
    is_gemini_model = "gemini" in model_name.lower()

    if is_openai_model:
        # OpenAI specific configuration
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        final_api_key = os.environ.get("OPENAI_API_KEY")
        if not final_api_key:
             print("WARNING: OPENAI_API_KEY not found in environment variables.")
    else:
        # Existing logic for Gemini/Local/Other
        if base_url is None:
            # Check if BASE_URL is in env
            env_base_url = os.environ.get("BASE_URL")
            if env_base_url:
                base_url = env_base_url
            else:
                base_url = f"{protocol}://{ip}:{port}/v1"
        
        # Priority: Argument > API_KEY env > GOOGLE_API_KEY env > "EMPTY"
        final_api_key = api_key or os.environ.get("API_KEY") or os.environ.get("GOOGLE_API_KEY") or "EMPTY"
    
    # Default model from env if not provided or stuck on default (Only for Gemini scenarios usually)
    if model_name == 'rednote-hilab/dots.ocr' and os.environ.get("GEMINI_MODEL"):
         model_name = os.environ.get("GEMINI_MODEL")

    client = OpenAI(api_key=final_api_key, base_url=base_url)
    
    # Prompt adjustment
    # Both Gemini via OpenAI connector and Native OpenAI GPT should use plain text prompt
    if is_gemini_model or is_openai_model:
        text_content = prompt
    else:
        text_content = f"<|img|><|imgpad|><|endofimg|>{prompt}"

    messages = []
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url":  PILimage_to_base64(image)},
                },
                {"type": "text", "text": text_content} 
            ],
        }
    )
    
    max_retries = 8
    base_delay = 5 # seconds

    try:
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    messages=messages, 
                    model=model_name, 
                    max_completion_tokens=max_completion_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
                break # Success
            except Exception as e:
                # Check for rate limit error (usually 429)
                if "429" in str(e) or "quota" in str(e).lower():
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                         delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                         print(f"Rate limited (429). Retrying in {delay}s...")
                         time.sleep(delay)
                         continue
                raise e # Re-raise other errors or if retries exhausted

        response_content = response.choices[0].message.content
        
        # Clean up markdown formatting if present (common with Gemini)
        if response_content.startswith("```json"):
            response_content = response_content[7:]
        elif response_content.startswith("```"):
            response_content = response_content[3:]
        
        if response_content.endswith("```"):
            response_content = response_content[:-3]
            
        return response_content.strip()
    except requests.exceptions.RequestException as e:
        print(f"request error: {e}")
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None

