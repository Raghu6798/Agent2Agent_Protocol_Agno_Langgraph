import os
from dotenv import load_dotenv
import asyncio
from typing import AsyncIterable, Dict, Any
from uuid import uuid4

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openrouter import OpenRouter
from llama_index.core.tools import FunctionTool

from together import Together
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import requests
from loguru import logger

load_dotenv()

# Initialize clients
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

llm = OpenRouter(
    model="meta-llama/llama-3.3-8b-instruct:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_tokens=512,
    context_window=4096,
    is_function_calling_model=True
)

def generate_image(prompt: str) -> str:
    """
    Generates and displays an image based on the provided text prompt using Together AI.
    
    Args:
        prompt (str): A descriptive text prompt for image generation
        
    Returns:
        str: Success or error message with image URL
    """
    try:
        print(f"🖼️ Generating image with prompt: {prompt}")
        
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            steps=1,
            n=1
        )
        
        url = response.data[0].url
        print(f"✅ Image generated successfully! URL: {url}")
        
        # Download and display the image
        img_response = requests.get(url)
        image = Image.open(BytesIO(img_response.content))
        
        plt.figure(figsize=(10, 8))
        plt.imshow(image)
        plt.axis('off')
        plt.title("Generated Brand Image")
        plt.show()
        
        return f"Image generated successfully and displayed. Direct URL: {url}"
        
    except Exception as e:
        error_msg = f"Error generating image: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def create_marketing_prompt(product_name: str, description: str, brand_colors: str, visual_style: str) -> str:
    """
    Creates an optimized marketing image prompt based on product specifications.
    
    Args:
        product_name (str): Name of the product
        description (str): Detailed product description
        brand_colors (str): Brand color palette (hex codes or color names)
        visual_style (str): Desired visual aesthetic and style
        
    Returns:
        str: Professionally crafted image generation prompt
    """
    try:
        print(f"📝 Creating marketing prompt for {product_name}...")
        
        # Create a focused, marketing-oriented prompt
        marketing_prompt = f"""
Premium {product_name} product photography: {description}. 
Styled as {visual_style} aesthetic with {brand_colors} color palette. 
Professional studio lighting, elegant composition, high-end commercial photography, 
clean background, artistic product placement, luxury branding visual.
"""
        
        # Clean up the prompt
        cleaned_prompt = " ".join(marketing_prompt.split())
        
        print(f"✅ Marketing prompt created: {cleaned_prompt}")
        return cleaned_prompt
        
    except Exception as e:
        error_msg = f"Error creating prompt: {str(e)}"
        print(f"❌ {error_msg}")
        # Return a fallback prompt
        return f"Professional {product_name} product photography with elegant lighting and premium styling"

def generate_brand_image_complete(product_name: str, description: str, brand_colors: str, visual_style: str) -> str:
    """
    Complete brand image generation workflow: creates prompt and generates image.
    
    Args:
        product_name (str): Name of the product
        description (str): Product description
        brand_colors (str): Brand color palette
        visual_style (str): Visual style preferences
        
    Returns:
        str: Complete workflow result with image URL
    """
    try:
        print(f"🚀 Starting complete brand generation for {product_name}")
        
        # Step 1: Create marketing prompt
        prompt = create_marketing_prompt(product_name, description, brand_colors, visual_style)
        
        # Step 2: Generate image using the prompt
        result = generate_image(prompt)
        
        return f"Brand generation completed for {product_name}. {result}"
        
    except Exception as e:
        error_msg = f"Complete workflow error: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

class BrandImageAgent:
    def __init__(self):
        self.agent = FunctionAgent(
            tools=[
                FunctionTool.from_defaults(fn=generate_image),
                FunctionTool.from_defaults(fn=create_marketing_prompt),
                FunctionTool.from_defaults(fn=generate_brand_image_complete)
            ],
            llm=llm,
            system_prompt="""You are a professional brand and marketing image generation assistant. 

You have access to three specialized tools:
1. create_marketing_prompt: Creates optimized prompts for product marketing images
2. generate_image: Generates images from text prompts using AI
3. generate_brand_image_complete: Complete workflow that creates prompt and generates image

When a user provides product details, use generate_brand_image_complete to handle the entire process automatically.

Always be helpful, professional, and focus on creating high-quality marketing visuals.""",
        )

    def invoke(self, query: str, session_id: str = None) -> str:
        """
        Synchronous method to invoke the brand image agent.
        
        Args:
            query (str): User query for brand image generation
            session_id (str): Optional session identifier for conversation tracking
            
        Returns:
            str: Agent response
        """
        if session_id is None:
            session_id = str(uuid4())
            
        logger.info(f"Invoking agent with query: {query}")
        
        try:
            # Run the agent synchronously
            response = asyncio.run(self.agent.run(query))
            
            # Extract the content from the response
            if hasattr(response, 'content'):
                return response.content
            elif hasattr(response, 'response'):
                return response.response
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"Error in invoke: {e}")
            return f"Error occurred: {str(e)}"

    async def stream(self, query: str, session_id: str = None) -> AsyncIterable[Dict[str, Any]]:
        """
        Asynchronous streaming method for the brand image agent.
        
        Args:
            query (str): User query for brand image generation
            session_id (str): Optional session identifier for conversation tracking
            
        Yields:
            Dict[str, Any]: Streaming response chunks with status updates
        """
        if session_id is None:
            session_id = str(uuid4())
            
        logger.info(f"Starting stream for query: {query}")
        
        try:
            # Initial status
            yield {
                'is_task_complete': False,
                'require_user_input': False,
                'content': 'Starting brand image generation...',
            }
            
            # Check if this is a complete workflow request
            if any(keyword in query.lower() for keyword in ['product', 'brand', 'generate', 'image']):
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Analyzing product requirements...',
                }
                
                # Simulate processing steps
                await asyncio.sleep(0.5)
                
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Creating marketing prompt...',
                }
                
                await asyncio.sleep(0.5)
                
                yield {
                    'is_task_complete': False,
                    'require_user_input': False,
                    'content': 'Generating brand image...',
                }
            
            # Run the agent
            response = await self.agent.run(query)
            
            # Extract content
            if hasattr(response, 'content'):
                content = response.content
            elif hasattr(response, 'response'):
                content = response.response
            else:
                content = str(response)
            
            # Final response
            yield {
                'is_task_complete': True,
                'require_user_input': False,
                'content': content,
            }
            
        except Exception as e:
            logger.error(f"Error in stream: {e}", exc_info=True)
            yield {
                'is_task_complete': True,
                'require_user_input': False,
                'content': f'An error occurred during brand image generation: {str(e)}',
            }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']

# Example usage
async def main():
    try:
        # Initialize the agent
        brand_agent = BrandImageAgent()
        
        print("🎨 Brand Image Generation Assistant")
        print("-" * 40)
        
        # Example with invoke method
        print("\n=== Testing Invoke Method ===")
        query = """
Please generate a professional brand marketing image for my product with these details:

Product Name: EcoWater Bottle
Description: Sustainable stainless steel water bottle with temperature control
Brand Colors: Green and silver
Visual Style: Modern minimalist

Use your complete workflow to create and generate the image.
"""
        
        result = brand_agent.invoke(query)
        print(f"Invoke Result: {result}")
        
        # Example with stream method
        print("\n=== Testing Stream Method ===")
        async for chunk in brand_agent.stream(query):
            print(f"Stream Chunk: {chunk}")
        
    except Exception as e:
        print(f"❌ Main execution error: {e}")
        import traceback
        traceback.print_exc()

# Run the agent
if __name__ == "__main__":
    asyncio.run(main())