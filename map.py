def get_spn(toponym):
    if "boundedBy" in toponym:
        lower_corner = list(map(float, toponym["boundedBy"]["Envelope"]["lowerCorner"].split()))
        upper_corner = list(map(float, toponym["boundedBy"]["Envelope"]["upperCorner"].split()))

        dx = abs(upper_corner[0] - lower_corner[0])
        dy = abs(upper_corner[1] - lower_corner[1])
        return str(dx), str(dy)

    return "0.005", "0.005"
