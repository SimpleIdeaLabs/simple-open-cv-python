import cv2, time, datetime, pandas

firstFrame = None
statusList = [None, None]
times = []
video = cv2.VideoCapture(0)
dataFrame = pandas.DataFrame(
  columns=[
    "Start", "End"
  ]
)

while True:
  check, frame = video.read()
  status = 0
  grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  grayFrame = cv2.GaussianBlur(grayFrame, (21, 21), 0)

  if firstFrame is None:
    firstFrame = grayFrame
    continue

  deltaFrame = cv2.absdiff(firstFrame, grayFrame)
  threshFrame = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
  threshFrame = cv2.dilate(threshFrame, None, iterations=2)

  (cnts,_) = cv2.findContours(threshFrame.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  for contour in cnts:
    if cv2.contourArea(contour) < 1000:
        continue
    status = 1
    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

  statusList.append(status)
  
  if statusList[-1]==1 and statusList[-2]==0:
    times.append(datetime.datetime.now())

  if statusList[-1]==0 and statusList[-2]==1:
    times.append(datetime.datetime.now())

  cv2.imshow("Color Frame", frame)

  key=cv2.waitKey(1)

  if key == ord("q"):
    if status == 1:
      times.append(datetime.datetime.now())
    break

# Generate Data Frame
for i in range(0, len(times), 2):
  dataFrame = dataFrame.append({
    "Start": times[i],
    "End": times[i+1]
  }, ignore_index=True)

dataFrame.to_csv("times.csv")

print(times)
video.release()
cv2.destroyAllWindows()
