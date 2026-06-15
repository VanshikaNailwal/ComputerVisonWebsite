from ultralytics import YOLO


helmet = YOLO(
    "storage/models/helmet.pt"
)


fire = YOLO(
    "storage/models/fireSmoke.pt"
)



print(
    helmet.names
)


print(
    fire.names
)