import zmq


def calculate_target_heart_rate(age):
    max_heart_rate = 208 - (0.7 * age)
    moderate_intensity = (max_heart_rate * 0.5, max_heart_rate * 0.7)
    vigorous_intensity = (max_heart_rate * 0.7, max_heart_rate * 0.85)
    return round(moderate_intensity[0]), round(moderate_intensity[1]), round(vigorous_intensity[0]), round(vigorous_intensity[1])


def determine_intensity(age, heart_rate):
    moderate_min, moderate_max, vigorous_min, vigorous_max = calculate_target_heart_rate(age)
    if heart_rate < moderate_min:
        return "light"
    elif moderate_min <= heart_rate < vigorous_min:
        return "moderate"
    elif vigorous_min <= heart_rate:
        return "vigorous"
    else:
        return "out of range"


def get_heart_rate_info():
    return ("If you do not have a device that checks your heart rate for you, you can check it manually. "
            "Use 2 fingers to find the pulse on the thumb side of the inside (palm side) of your wrist. "
            "Count the beats for 30 seconds, then multiply by 2 to get your heart rate in bpm.")


# Setting up the ZeroMQ server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Heart rate microservice is running...")

while True:
    # Wait for the next request from the client
    message = socket.recv_string()
    print(f"Received request: {message}")

    # Parse the request
    parts = message.split()
    request_type = parts[0]
    age = int(parts[1]) if len(parts) > 1 and parts[1] != "xxx" else None
    heart_rate = int(parts[2]) if len(parts) > 2 and parts[2] != "xxx" else None

    # Process the request
    if request_type == "H" and age is not None and heart_rate is not None:
        intensity = determine_intensity(age, heart_rate)
        response = f"Your exercise intensity is {intensity}."
    elif request_type == "T":
        response = get_heart_rate_info()
    elif request_type == "C" and age is not None:
        moderate_min, moderate_max, vigorous_min, vigorous_max = calculate_target_heart_rate(age)
        response = f"Your target heart rate for moderate intensity is {moderate_min}-{moderate_max} bpm and for vigorous intensity is {vigorous_min}-{vigorous_max} bpm."
    else:
        response = "Invalid request. Please check your input."

    # Send the response back to the client
    socket.send_string(response)