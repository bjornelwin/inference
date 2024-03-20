import cv2
from inference_models import yolo
from read_classes_and_colors import ClassesAndColors
import numpy as np



def draw_boxes(frame, boxes, scores, classes, class_names, color_pans):
    boxed_image = np.copy(frame)
    for i in range(len(boxes)):
        box = boxes[i]
        ymin, xmin, ymax, xmax = box
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        class_index = int(classes[i])
        class_name = class_names[class_index]
        print(color_pans)
        print(class_index % len(color_pans))
        color = color_pans[class_index % len(color_pans)]
        cv2.rectangle(boxed_image, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(boxed_image, f"{class_name} {scores[i]:.2f}", (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return boxed_image
        
def main():
    # Initialize the USB camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    # Set the width and height of the video capture
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    model =  yolo()
    coco_classes, color_pans = ClassesAndColors()
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is captured successfully
        if not ret:
            print("Error: Unable to capture frame")
            break
        print(type(frame))
        boxes, scores, classes = model.infer(frame) 
        box_frame = draw_boxes(frame, boxes, scores, classes, coco_classes, color_pans)
        # Display the frame
        cv2.imshow('USB Camera Stream', box_frame)
        key = cv2.waitKey(1)
        # Check for 'q' key press to exit
        if key & 0xFF == ord('q'):
            break
            
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
