from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from . import schemas
from . import services as video_services

router = APIRouter(
    prefix="/v1",
    tags=["v1/videos"],
)


@router.post("/videos",  status_code=201, responses={
            201: {'model': schemas.UploadVideoSuccessResponse},
            413: {"model": schemas.VideoTooLargeResponse}})
async def upload_video(file: UploadFile):
    result = await video_services.upload_video(file)
    return schemas.UploadVideoSuccessResponse(**result)

@router.get("/videos/{video_id}",  status_code=200, responses={
            200: {'model': schemas.AnalyzedResponse},
            202: {"model": schemas.NotYetAnalyzedResponse}})
async def get_video(video_id: str, is_analyzed: bool = False):
    """
    Get the analysis results of the video.

    This function will get the analysis results from the video. Depending on whether the video has been analyzed or not, two different results will be returned.


    Parameters:
    1. video_id (str): A unique video id.
    2. is_analyzed (bool): If is_analyzed is False, the api will return un analyzed results. If is_analyzed is True, the api will return the analysis results of the video. This variable is used to let the frontend test the 2 results returned by the api.

    Returns:
    1. schemas.AnalyzeResponse: The generated payload data.
    2. schemas.NotYetAnalyzedResponse: If the video is being analyzed, there are no results yet.

    The function performs the following steps:
    1. Defines possible pollution levels and item categories.
    2. Randomly selects a number of items and assigns them categories and scores.
    3. Calculates the total environmental score and determines the pollution level.
    4. Constructs the payload data including the identifier, item details, and overall scores.
    5. Sends the payload to the specified callback URL via an asynchronous POST request.
    6. Returns the payload data.

    Field Descriptions:
    - _id (str): A unique identifier for this particular webhook event.
    - status(str): Done or processing.
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
        video_id = "12345"
        await get_video(video_id, is_analyzed)

    The payload data structure:
    {
        '_id': str,
        'status': str,
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
    results = await video_services.get_video(video_id, is_analyzed)
    if is_analyzed is False:
        response = schemas.NotYetAnalyzedResponse(**results).model_dump()
        return JSONResponse(status_code=202, content=response)
    return schemas.AnalyzedResponse(**results)