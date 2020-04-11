import cv2
import os
from detectors import YoloDetector

# path to directory with yolov3.cfg and yolov3.weights
model_path = ".../yolo-coco"

# there are 1000 frames from each of the cameras
number_of_photos = 1000

# set counter to X if you want to skip X first frames
counter = 0

# change camera's id (12 or 15)
camera = "12"

print("Number of people you see on the screen: ")
while counter != number_of_photos:
    # there are 6 frames for each second
    second = str(counter // 6)
    num_frame = str(counter % 6)
    name = "c" + camera + "_20191122_1900_" + second + "_" + num_frame
    print("Processing: ", name + ".jpg")

    # display image
    image = cv2.imread(name + ".jpg")
    # cv2.imshow(name, image)

    # press any key to close image window
    cv2.waitKey(0)

    # input number of people you see on the screen
    num_of_people = input("Input number of people you see on the screen: ")

    # if there are 0 people on screen delete both files linked with this frame
    if num_of_people == '0':
        os.remove(name + ".jpg")
        os.remove(name + ".txt")
    else:
        # get YOLO's predictions
        detector = YoloDetector(model_path)
        detection_output = detector.detect(image)
        predicted_number = str(len(detection_output[0]))

        # save both numbers in .txt file
        fin = open(name + ".txt", 'w')
        print(predicted_number + " " + num_of_people, file=fin)
        fin.close()

    counter += 1

print("Processing finished successfully")
