import cv2

import numpy as np

thresh = 0.5

net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

cap = cv2.VideoCapture(0)
classes = []
classFile = 'coco.names'
with open(classFile, 'r') as f:
    classes = f.read().splitlines()

a = np.array([[2.2, 3.7, 9.1], [4, 3.1, 1.3]])

b = np.argmax(a[:, 1:], axis=1)

c = a[0]

a[:, [0, 2]] = (a[:, [0, 2]] * 3).astype(int)

print(a)
# print((a[:,[0,2]]*3).astype(int))

while True:
    ret, img = cap.read()

    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True)

    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # print(layer_outputs)
    boxes = np.array([])
    class_ids = np.array([])
    confidences = np.array([])

    # print(len(layer_outputs[0][0]))

    for output in layer_outputs:
        # print(np.max(output,axis=0))

        temp_scores = np.copy(output[:, 5:])
        temp_class_ids = np.argmax(temp_scores, axis=1)
        #print(temp_scores)
        ids = np.arange(len(temp_class_ids))
        temp_confidences = temp_scores[ids, temp_class_ids]

        temp_boxes = np.copy(output[:, :4])
        # print(temp_boxes[:,[0,2]])
        temp_boxes[:, [0, 2]] = (temp_boxes[:, [0, 2]] * width)
        temp_boxes[:, [1, 3]] = (temp_boxes[:, [1, 3]] * height)
        temp_boxes[:, 0] = (temp_boxes[:, 0] - temp_boxes[:, 2] / 2)
        temp_boxes[:, 1] = (temp_boxes[:, 1] - temp_boxes[:, 3] / 2)

        indices = temp_confidences > thresh
        # print(temp_scores[indices])
        if len(boxes) == 0:
            boxes = temp_boxes[indices]
            confidences = temp_confidences[indices]
            class_ids = temp_class_ids[indices]
        elif len(indices) == 0:
            pass
        else:
            boxes = np.concatenate((boxes, temp_boxes[indices]), axis=0)
            confidences = np.concatenate((confidences, temp_confidences[indices]), axis=0)
            class_ids = np.concatenate((class_ids, temp_class_ids[indices]), axis=0)

        # for detection in output:
        #     scores = detection[4:]
        #     scores[0]=0
        #     class_id = np.argmax(scores)
        #     confidence = scores[class_id]


            # if confidence > thresh:
            #     print(class_id)
            #     print(scores)
        #         center_x = int(detection[0] * width)
        #         center_y = int(detection[1] * height)
        #         w = int(detection[2] * width)
        #         h = int(detection[3] * height)
        #
        #         x = int(center_x - w / 2)
        #         y = int(center_y - h / 2)
        #         boxes.append([x, y, w, h])
        #         #print(boxes)
        #         confidences.append(float(confidence))
        #         class_ids.append(class_id)

    # print(len(boxes))

    boxes = boxes.astype(int)
    # print(boxes)
    confidences = confidences.astype(float)
    # print(confidences)
    # print(class_ids)
    boxes = boxes.tolist()
    confidences = confidences.tolist()

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, thresh, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN

    #colors = np.random.uniform(0, 255, size=(len(boxes), 3))

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            # print(x, y, w, h)
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = (0,200,0)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

    cv2.imshow('Input', img)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
