from datetime import datetime
import os
from google import genai
from google.genai import types
from google.adk.tools import ToolContext
from .... import config  # Make sure config.IMAGE_FOLDER exists and is correctly set

client = genai.Client(vertexai=False)

async def generate_images(imagen_prompt: str, tool_context: ToolContext):
    try:
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=imagen_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                safety_filter_level="block_low_and_above",
                person_generation="allow_adult",
            ),
        )

        if response.generated_images is not None:
            for generated_image in response.generated_images:
                image_bytes = generated_image.image.image_bytes
                counter = str(tool_context.state.get("loop_iteration", 0))
                artifact_name = f"generated_image_{counter}.png"

                # Save locally
                local_path = save_to_local(tool_context, image_bytes, artifact_name, counter)

                # Save as ADK artifact (optional, for downstream tools)
                report_artifact = types.Part.from_bytes(
                    data=image_bytes, mime_type="image/png"
                )
                await tool_context.save_artifact(artifact_name, report_artifact)

                print(f"✅ Image saved locally: {local_path}")
                print(f"🧠 Image also saved as ADK artifact: {artifact_name}")

                return {
                    "status": "success",
                    "message": f"Image saved locally and registered as artifact: {artifact_name}",
                    "artifact_name": artifact_name,
                }
        else:
            error_details = str(response)
            print(f"⚠️ No images generated. Response: {error_details}")
            return {
                "status": "error",
                "message": f"No images generated. Response: {error_details}",
            }

    except Exception as e:
        return {"status": "error", "message": f"Image generation failed: {e}"}


# ✅ Replace GCS upload with local save
def save_to_local(tool_context: ToolContext, image_bytes, filename: str, counter: str):
    # Get session ID and date
    unique_id = tool_context.state.get("unique_id", "default_session")
    current_date_str = datetime.utcnow().strftime("%Y-%m-%d")

    # Construct local path (e.g., generated_images/2025-08-03/default_session/filename.png)
    local_dir = os.path.join(config.IMAGE_FOLDER, current_date_str, unique_id)
    os.makedirs(local_dir, exist_ok=True)

    local_file_path = os.path.join(local_dir, filename)

    # Save image
    with open(local_file_path, "wb") as f:
        f.write(image_bytes)

    # Store file path in session context
    tool_context.state["generated_image_local_path_" + counter] = local_file_path

    return local_file_path
