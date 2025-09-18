import cv2
import numpy as np

# ! Non provato

# loading the images for building the database
images = []

img = cv2.imread("Esercitazioni\opencv_lessons\data\dnd.jpg")
images.append(img)

img = cv2.imread("Esercitazioni\opencv_lessons\data\\tomb.jpg")
images.append(img)

img = cv2.imread("Esercitazioni\opencv_lessons\data\ghost.jpg")
images.append(img)

# creating the list containing the classes of the objects
classes = ["DnD", "Tomb Raider", "Ghost"]

# creating the descriptors database
def descriptorDB(images):
    descriptor_list = []
    
    orb = cv2.ORB.create(nfeatures=1000)

    # extract features from each loaded image
    for image in images:
        _, descr = orb.detectAndCompute(image, None)
        descriptor_list.append(descr) 
    
    return descriptor_list

# do the match
def objClassification(frame, descriptor_list):
    orb = cv2.ORB.create(nfeatures=1000)

    _, descr = orb.detectAndCompute(frame, None)

    # create the matcher
    matcher = cv2.BFMatcher.create()
    best_matches = []

    # perform the matches with the database
    for descriptor in descriptor_list:
        matches = matcher.knnMatch(descr, descriptor, k=2)
        good = []

        for m, n in matches:
            if m.distance < n.distance * 0.8:
                good.append(m)

        best_matches.append(len(good))

    # classID
    classID = -1

    if len(best_matches) > 0:
        max_val = max(best_matches)
        if max_val > 10:
            classID = best_matches.index(max_val)
    
    return classID

# let's see if it works
descriptor_list = descriptorDB(images)
webcam = cv2.VideoCapture(0)

while True:
    success, frame = webcam.read()

    classID = objClassification(frame, descriptor_list)


    if classID != -1:
        cv2.putText(frame, classes[classID], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
    
    cv2.imshow("webcam", frame)
    key = cv2.waitKey(30)

    if key == ord('q'):
        quit()
