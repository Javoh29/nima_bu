import base64

with open("nuron_logo.png", "rb") as f:
    for line in f.readlines(256):
        print(base64.b64encode(line).decode("utf-8"))