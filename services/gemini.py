import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

from configs.settings import settings
from models.file import File

vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.LOCATION)


class GeminiService:
    def __init__(
        self,
    ):
        self.model = GenerativeModel(model_name=settings.GEMINI_MODEL_NAME)
        self.stream = True
        self.generation_config = {"temperature": 0.3, "max_output_tokens": 2048}

    def get_gemini_response(self, prompt: str, file: File) -> list[str]:
        file_uri = (
            f"gs://file-drive-uploads-{settings.GOOGLE_CLOUD_PROJECT}/{file.name}"
        )
        file = Part.from_uri(uri=file_uri, mime_type=file.mime_type)
        contents = [prompt, file]

        responses = self.model.generate_content(
            contents=contents,
            generation_config=self.generation_config,
            stream=self.stream,
        )

        final_response = []

        for response in responses:
            try:
                final_response.append(response.text)
            except IndexError:
                final_response.append("")
                continue

        return " ".join(final_response)
