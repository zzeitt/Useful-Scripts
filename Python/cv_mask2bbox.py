def binary_mask_to_box(binary_mask):
    binary_mask = np.array(binary_mask, np.uint8)
    contours, hierarchy = cv2.findContours(
        binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areas.append(area)
    # 取最大面积的连通区域
    idx = areas.index(np.max(areas))
    x, y, w, h = cv2.boundingRect(contours[idx])
    bounding_box = [x, y, x+w, y+h]

    return bounding_box
