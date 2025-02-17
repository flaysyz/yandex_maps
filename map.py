def calculate_spn(bounding_box):
    if bounding_box:
        lon_diff = abs(bounding_box[1][0] - bounding_box[0][0])
        lat_diff = abs(bounding_box[1][1] - bounding_box[0][1])
        return f"{lon_diff},{lat_diff}"
    return "0.005,0.005"
