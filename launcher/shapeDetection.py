import numpy as np
import json
import cv2

def detect_shape(contour):
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    if len(approx) == 2:
        return "platform"   
    if len(approx) == 3:
        return "coin"       
    # elif len(approx) == 4:
    #     return "wall"     
    elif len(approx) == 5:
        return "spawn"       
    elif len(approx) == 6:
        return "exit"
    # elif len(approx) > 5:
    #     return "coin"       
    
    return "unknown"

def process(img_name):
    # Load or capture the image
    img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
    # img = cv2.resize(org, (16, 16))
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)  # Invert so shapes are white on black


    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shape_data = []
    for contour in contours:
        
        shape = detect_shape(contour)
        print(shape)

        if shape == "unknown":
            continue

        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        lx, ly, w, h = cv2.boundingRect(contour)
        type_ = shape 

        shape_data.append({
            "type": shape,
            "cx": cx,
            "cy": cy,
            "lx": lx,
            "ly": ly,
            "width": w,
            "height": h
        })

    return shape_data

    # with open("map.json", "w") as f:
    #     json.dump(shape_data, f)
