import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2

cap = cv2.VideoCapture(0) # Connect to laptop webcam using 0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
 


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('converted_keras/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


# Replace this with the path to your image

size = (224, 224)
count=0
while True:
    ret,frame = cap.read()#returns a tuple where frame is what is shown in the webcam
    
    image = cv2.resize(frame, size)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    max_probab = max(prediction[0])
    if(prediction[0][0]==max_probab):
        move = "UP"
    elif(prediction[0][1]==max_probab):
        move = "DOWN"
    else:
        move = "STRAIGHT"
    count=(count+1)%10
    if(count<=9):
        cv2.putText(frame,'MOVE:'+move,(10,160), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),3,cv2.LINE_AA)
        print(move)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):#wait one sec and check if 'q' pressed.
        break
cap.release()

cv2.destroyAllWindows()


