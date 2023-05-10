import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
model_path = './hand_landmarker.task'
import time
import pypiano
from mingus.containers import Note
piano=pypiano.Piano(audio_driver='pulseaudio')

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

video_capture = cv2.VideoCapture(1)
# video_capture = cv2.VideoCapture("http://192.168.137.226:8080/video")

joints={
        # 'thumb':[4,3],
        'index':[8,10],
        'middle':[12,14],
        'ring':[16],
        'pinky':[20],
        }

# Notes=['c','C','d','D','e','E','f','F','g','G','h','a','A','b','B','c','C']
# Notes=['C','C#','D','D#','E','E','f','F','g','G','h','a','A','b','B','c','C']
Notes = [[
    'C',
    'C#',
    'D',
    'D#',
    'E',
    'F',
    ],
    [
    'F#',
    'G',
    'G#',
    'A',
    'A#',
    'B',
    ]
         
]

flags=np.ones((2,6))
thres_l=0.2
thres_h=0.2
MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green
frame_out=None
# coords=np.zeros((len(joints.keys()),2,3))
def required_coords(landmarks):
  coords=[]
  thumbs=np.array([landmarks[4].x,landmarks[4].y,landmarks[4].z])
  # thumbs=0
  for i,key in enumerate(joints):
    a=[]
    for j in range(len(joints[key])):
      a.append(np.array([landmarks[joints[key][j]].x,landmarks[joints[key][j]].y,landmarks[joints[key][j]].z]))
    # a1=np.array([landmarks[joints[key][0]].x,landmarks[joints[key][0]].y,landmarks[joints[key][0]].z])
    # a2=np.array([landmarks[joints[key][1]].x,landmarks[joints[key][1]].y,landmarks[joints[key][1]].z])
    a=np.array(a)
    print(a.shape)
    coords.append(a.reshape(-1,3))
  return np.concatenate(coords,axis=0),thumbs

def draw_landmarks_on_image(detection_result: HandLandmarkerResult, rgb_image: mp.Image, timestamp_ms: int):
  global frame_out
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  # print("SHAPE:",rgb_image.numpy_view().shape)
  # img=detection_result.output_image
  annotated_image = np.copy(rgb_image.numpy_view())
  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]
    print("HAND:",handedness)
    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    print("REACHDEDHERE!!")
    rel_coords,thumbs=required_coords(hand_landmarks)
    print("SHAPEE::",rel_coords.shape)
    rel_coords=rel_coords.reshape(-1,3)
    dists=np.linalg.norm(rel_coords-thumbs,axis=-1)
    # print("DISTANCE",dists.shape,rel_coords.shape,thumbs.shape)
    min_idx=np.argmin(dists)
    min_val=dists[min_idx]
    # print(flags,min_idx,flags[min_idx],min_val)
    # print(flags[min_idx]==1,min_val<thres_l)
    if min_val<thres_l and flags[idx][min_idx]==1:
      print("NOTE:",Notes[idx][min_idx],min_val)
      # piano.play(Note.from_shorthand(Notes[min_idx]))
      note=Note(Notes[idx][min_idx],4,velocity=127,channel=15)
      # piano.play(Notes[min_idx])
      flags[idx][min_idx]=0
      piano.play(note)
    # print("REACHED_HERE",rel_coords)
    flags[idx][dists>=thres_h]=1
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style()
      )
    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  frame_out=annotated_image
  # return annotated_image

# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=draw_landmarks_on_image,
    num_hands=2)
t_start=time.time()

with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        t=int(1000*(time.time()-t_start))
        frame_out=None
        ret,frame=video_capture.read()
        frame=cv2.flip(frame,1)
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result=landmarker.detect_async(mp_image, t)
        # img=landmarker.callback(,t)
        # mp.ta
        # if img is None:
          # print("None returned")
          # img=frame
        if frame_out is None:
          frame_out=frame
        cv2.imshow('MediaPipe Hands', frame_out[...,::-1])
        key=cv2.waitKey(1)
        if key==ord('q'):
            exit(0)
        
        # landmarker.callback = draw_landmarks_on_image
