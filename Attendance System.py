from tkinter import *
import face_recognition
import cv2 as cv
import numpy as np

root=Tk()
root.geometry("850x540")
root.title("Attendence System")

Label(text='Attendence System\n', font="comicsansms 15 bold underline",pady=15,fg="Black").pack()

def attendance():
    video_capture = cv.VideoCapture(0)

    my_image = face_recognition.load_image_file("test.jpg")
    my_face_encoding = face_recognition.face_encodings(my_image)[0]

    elon_image = face_recognition.load_image_file("elon.jpg")
    elon_face_encoding = face_recognition.face_encodings(elon_image)[0]

    shreya_image = face_recognition.load_image_file("shreya.jpg")
    shreya_face_encoding = face_recognition.face_encodings(shreya_image)[0]
    
    pusp_image = face_recognition.load_image_file("pusp.jpg")
    pusp_face_encoding = face_recognition.face_encodings(pusp_image)[0]

    known_face_encodings = [
        my_face_encoding,
        elon_face_encoding,
        shreya_face_encoding,
        pusp_face_encoding
    ]
    known_face_names = [
        "Nishant",
        "Elon",
        "Shreya",
        "Pushpraj"
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        gray = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)

        if process_this_frame:
            face_locations = face_recognition.face_locations(gray)
            face_encodings = face_recognition.face_encodings(gray, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
            font = cv.FONT_HERSHEY_DUPLEX
            cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            with open("records.txt","a") as f:
                f.write(name+',')

        cv.imshow('Face recognition', frame)
        if cv.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv.destroyAllWindows()
    
    from datetime import date
    today = date.today()

    my_file = open("records.txt", "r")
    content = my_file.read()
    content_list = content.split(",")
    my_file.close()
    #print(content_list)
    toset = set(content_list)
    tolist = list(toset)
    tolist.remove('')
    if 'Unknown' in tolist:
        tolist.remove('Unknown')
    print(tolist)
    with open("present.txt","a") as f:
        d = today.strftime('''%B %d, %Y 
--------------------------\n''')
        f.write(d)

        for i in tolist:
            f.write(i+",\n")
        f.write('\nTotal Attendance: '+str(len(tolist))+'\n')

    txt = "Number of student present : " + str(len(tolist))
    Label(root,text=txt, font="comicsansms 15",pady=45,fg="Black").pack()
        
Button(text="Take Attendance",command=attendance).pack()

root.mainloop()