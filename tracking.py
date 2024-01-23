import cv2
import numpy as np
import time

# TARGET = np.array([245, 252, 251])
# TARGET = np.array([146, 164, 254]) # rouge
TARGET = np.array([244, 255, 252]) # vert


THRESHOLD = 20
lower_red = TARGET - THRESHOLD
upper_red = TARGET + THRESHOLD
# lower_red = np.array([130, 115, 200])
# upper_red = np.array([180, 200, 255])

def track(file_path):
    cap = cv2.VideoCapture(file_path)


    file = open(file_path + ".csv", "w")
    file.write("t,x,y\n")

    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

    print("FPS: " + str(fps))

    previewShown = True
    frameIndex = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # rognage du frame si besoin
        # frame = frame[int(frame.shape[1] * 0.05):int(frame.shape[1] * 0.5), int(frame.shape[1] * 0.3):int(frame.shape[1] * 0.75)]

        if frameIndex == 0:
            # La première image est enregistrée pour y lire manuellement la couleur cible
            cv2.imwrite("out.png", frame)

        # Temps courant
        t = frameIndex / fps

        # Filtre par couleur
        mask = cv2.inRange(frame, lower_red, upper_red)

        # Detection de contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Tri des contours par taille de la zone
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        if len(sorted_contours) > 0:
            contour = sorted_contours[0]  # on s’intéresse au plus grand contour

            cv2.drawContours(frame, [contour], 0, (0, 0, 0), 1)

            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

                cv2.line(frame, (cx - 10, cy), (cx + 10, cy), (0, 0, 0), 1)
                cv2.line(frame, (cx, cy - 10), (cx, cy + 10), (0, 0, 0), 1)

                file.write(f"{t},{cx},{cy}\n")

        if previewShown:
            cv2.imshow("Mask", mask)
            cv2.imshow("Image", frame)

            key = cv2.waitKey(100)
            if key & 0xFF == ord("q"):
                exit(0)
            elif key & 0xFF == ord("h"):
                # Visualisation cachée pour aller plus vite
                previewShown = False

        if frameIndex % 50 == 0:
            print(f"{round(t)}s / {round(duration)}s")

        frameIndex += 1

    cap.release()
    cv2.destroyAllWindows()
    file.close()

def track_amplitude(file_path, frequency):
    dt = 1.0 / frequency
    print(frequency, dt)

    cap = cv2.VideoCapture(file_path)

    file = open(file_path + ".amplitude.csv", "w")
    file.write("t,a\n")

    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

    print("FPS: " + str(fps))

    previewShown = True
    frameIndex = 0

    prevTime = 0
    maxY = 0
    minY = 1000

    while True:
        ret, frame = cap.read()
        if not ret:
            break


        if frameIndex == 0:
            # La première image est enregistrée pour y lire manuellement la couleur cible
            cv2.imwrite("out.png", frame)

        # Temps courant
        t = frameIndex / fps

        # Filtre par couleur
        mask = cv2.inRange(frame, lower_red, upper_red)
        # Detection de contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Tri des contours par taille de la zone
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        if len(sorted_contours) > 0:
            contour = sorted_contours[0]  # on s’intéresse au plus grand contour
            cv2.drawContours(frame, [contour], 0, (0, 0, 0), 1)
            for point in contour:
                if point[0][1] > maxY:
                    maxY = point[0][1]
                if point[0][1] < minY:
                    minY = point[0][1]
        
        switched = False

        if (t - prevTime) > dt:
            file.write(f"{t},{maxY - minY}\n")
            
            try:
                cv2.line(frame, (0, maxY), (frame.shape[1], maxY), (255, 0, 0), 1)
                cv2.line(frame, (0, minY), (frame.shape[1], minY), (255, 0, 0), 1)
            except:
                pass
            switched = True
            prevTime = t
            maxY = 0
            minY = 99999999999

        # if previewShown:
        cv2.imshow("Mask", mask)
        cv2.imshow("Image", frame)

        if not previewShown:
            key = cv2.waitKey(1)
        elif switched:
            key = cv2.waitKey(500)
        else:
            key = cv2.waitKey(10)

        if key & 0xFF == ord("q"):
            exit(0)
        elif key & 0xFF == ord("h"):
            # Visualisation cachée pour aller plus vite
            previewShown = False
        

        if frameIndex % 50 == 0:
            print(f"{round(t)}s / {round(duration)}s")

        frameIndex += 1

    cap.release()
    cv2.destroyAllWindows()
    file.close()