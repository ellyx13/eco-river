import cv2
from ultralytics import YOLO
from . import config

model = YOLO("bestv2.pt")


async def determine_category(trash_name):
    trash_name_lower = trash_name.lower()
    
    for category, details in config.categories.items():
        if any(keyword in trash_name_lower for keyword in details["keywords"]):
            return category, details["score"]
    
    return 'unknown', config.categories["unknown"]["score"]


async def analyze_video(file_path) -> dict:
    cap = cv2.VideoCapture(file_path)
    assert cap.isOpened(), "Error reading video file"

    objects = {}
    frame_id = -1
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        frame_id += 1

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True)
        if results[0].boxes.id is None:
            continue
        # Get track IDs
        track_ids = results[0].boxes.id.int().cpu().tolist()
        names = list(results[0].names.values())
        for track_id in track_ids:
            if not objects.get(track_id):
                result = {}
                result['frame'] = frame_id
                result['name'] = names[0]
                result['category'], result['environment_score'] = await determine_category(names[0])
                objects.update({track_id: result})

    results = {}
    results['status'] = 'done'
    results['results'] = []
    results['total_items'] = 0
    results['total_environment_score'] = 0
    
    for obj in objects.values():
        results['total_items'] += 1
        results['total_environment_score'] += obj['environment_score']
        results['results'].append({'name': obj['name'], 'seconds': obj['frame'], 'category': obj['category'], 'environment_score': obj['environment_score']})
    
    if results['total_environment_score'] <= 20:
        pollution_level = "Low"
    elif results['total_environment_score'] <= 30:
        pollution_level = "Medium"
    else:
        pollution_level = "High"
        
    results['environmental_pollution_level'] = pollution_level
    
    return results
