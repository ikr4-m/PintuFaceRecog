import cv2
import face_recognition
import pickle
import os
import numpy as np
from decouple import config
from serial import Serial

# Buka serial arduino
#arduino = Serial(port=config('ARDUINO_PORT_SERIAL'), baudrate=9600, timeout=.1)

# Final variabel
DATASET_FOLDER_PATH = 'dataset'
DATASET_FILE_NAME = config('FACEREG_DATASET_NAME')
SAMPLING_FACE_JITTER = int(config('FACEREG_SAMPLING_JITTER'))
FRAME_SKIPPED = int(config('FACEREG_FRAME_SKIPPED'))
SAFE_FRAME_COUNT = FRAME_SKIPPED * 3

# Buat dataset apabila belum ada di folder dataset
if os.path.isfile(f'./{DATASET_FOLDER_PATH}/{DATASET_FILE_NAME}') != True:
    first_name_list = [x for x in os.listdir(DATASET_FOLDER_PATH) if os.path.isdir(f'./{DATASET_FOLDER_PATH}/{x}')]
    all_face_encodings = {}
    print(f'Get {len(first_name_list)} group name.')
    for x in first_name_list:
        file_path = f'./{DATASET_FOLDER_PATH}/{x}'
        file_list = [f'{file_path}/{xx}' for xx in os.listdir(file_path) if os.path.isdir(f'{file_path}/{xx}') is False]
        print(f'Get {x} name with {len(file_list)} face.')
        for image in file_list:
            key_name = f'{x}:{image.split("/").pop().split(".")[0]}'
            print(f'Resampling {key_name} with {SAMPLING_FACE_JITTER} times')
            image = face_recognition.load_image_file(image)
            all_face_encodings[key_name] = face_recognition.face_encodings(image, num_jitters=SAMPLING_FACE_JITTER)[0]
    print(f'Save the dataset to {DATASET_FILE_NAME}')
    with open(f'./{DATASET_FOLDER_PATH}/{DATASET_FILE_NAME}', 'wb') as f: pickle.dump(all_face_encodings, f)
    print('Training data done!')

# Setelah melakukan training dataset, kita mengambil semua dataset yang sudah ditrain
all_face_encodings = {}
with open(f'./{DATASET_FOLDER_PATH}/{DATASET_FILE_NAME}', 'rb') as f:
    all_face_encodings = pickle.load(f)

name_list = [x.split(':')[0] for x in list(all_face_encodings.keys())]
encode_image = np.array(list(all_face_encodings.values()))

# Inisialisasi variabel untuk menjalankan OpenCV2
video = cv2.VideoCapture(0)
face_locations = []
face_encodings = []
face_names = []
dump_face_name = {}
face_name_detected = []
frame_count = 0
print('Spawning CV2')


"""
Fungsi ini akan dijalankan apabila muka terdeteksi oleh sistem.
Cara kerjanya, setelah dideteksi dengan frame waktu tertentu,
sistem akan melakukan request ke server dan mengirim ID dataset
ke webserver.
"""
def verify_face(name: str) -> any:
    if name == 'Unknown': return
    if name in face_name_detected: return

    if name not in dump_face_name: dump_face_name[name] = 1
    else: dump_face_name[name] += 1
    if dump_face_name[name] == SAFE_FRAME_COUNT:
        face_name_detected.append(name)
        del dump_face_name[name]

# Jalankan deteksi muka
while True:
    frame = video.read()[1]
    frame_count += 1

    # Proses tiap FRAME_SKIPPED
    if frame_count % FRAME_SKIPPED == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encode_image, face_encoding, tolerance=0.45)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(encode_image, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = name_list[best_match_index]

            face_names.append(name)
        
        # Reset to 0 frame count so the int will not overloaded
        frame_count = 0

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        #if name == "Unknown": continue
        if name in face_name_detected: continue

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        #verify_face(name)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

video.release()
cv2.destroyAllWindows()