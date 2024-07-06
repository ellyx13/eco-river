from fastapi import APIRouter, UploadFile
from . import schemas
from . import services as video_services

router = APIRouter(
    prefix="/v1",
    tags=["v1/videos"],
)


@router.post("/videos/{identifier}",  status_code=201, responses={
            201: {'model': schemas.UploadVideoSuccessResponse},
            413: {"model": schemas.VideoTooLargeResponse}})
async def upload_video(identifier: str, file: UploadFile):
    await video_services.upload_video(identifier, file)
    return schemas.UploadVideoSuccessResponse()


@router.post("/videos/callback/webhook/fake",  status_code=201, responses={
            201: {'model': schemas.AnalyzeFakeResponse}})
async def generate_fake_webhook(identifier: str, url_callback: str):
    """
    Generate and send a fake analyze video webhook payload.

    This function creates a simulated payload for a webhook, including details
    about various items, their environmental scores, and overall pollution levels.
    The payload is sent to the specified callback URL using an asynchronous POST request.

    Parameters:
    identifier (str): A unique identifier for the webhook payload.
    url_callback (str): The URL to which the webhook payload will be sent.

    Returns:
    schemas.AnalyzeFakeResponse: The generated payload data.

    The function performs the following steps:
    1. Defines possible pollution levels and item categories.
    2. Randomly selects a number of items and assigns them categories and scores.
    3. Calculates the total environmental score and determines the pollution level.
    4. Constructs the payload data including the identifier, item details, and overall scores.
    5. Sends the payload to the specified callback URL via an asynchronous POST request.
    6. Returns the payload data.

    Field Descriptions:
    - identifier (str): A unique identifier for this particular webhook event.
    - total_items (int): The total number of items included in the webhook payload.
    - total_environment_score (int): The sum of the environment scores of all items.
    - environmental_pollution_level (str): The pollution level based on total_environment_score. 
      Possible values are:
        - "Low" if total_environment_score <= 20
        - "Medium" if total_environment_score <= 30
        - "High" if total_environment_score > 30
    - results (list): A list of dictionaries where each dictionary represents an item with the following fields:
        - name (str): The name of the item (e.g., "Plastic Bottle").
        - category (str): The category of the item (e.g., "Plastic").
        - environment_score (int): The environmental score of the item, ranging from 1 to 10.
        - seconds (int): The appearance time of the object in seconds.
        
    Example:
        identifier = "12345"
        url_callback = "http://example.com/webhook"
        await generate_fake_webhook(identifier, url_callback)

    The payload data structure:
    {
        'identifier': str,
        'total_items': int,
        'total_environment_score': int,
        'environmental_pollution_level': str,
        'results': [
            {
                'name': str,
                'category': str,
                'environment_score': int,
                'seconds': int
            },
            ...
        ]
    }
    """
    results = await video_services.generate_fake_webhook(identifier, url_callback)
    return schemas.AnalyzeFakeResponse(**results)