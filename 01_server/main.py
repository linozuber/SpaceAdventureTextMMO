from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from account import Account
import json

class Response():
    data = {
        "message" : "",
        "interaction" : ""
    }

    def __init__(self, _message, _interaction = ""):
        self.data["message"] = _message
        self.data["interaction"] = _interaction

class Serv(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        pass

    def do_POST(self):
        #'''Reads post request body'''
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))

        reply = executeCommand(post_data["userId"], post_data["interaction"], post_data["action"])
        self.wfile.write(bytes(reply, "utf-8"))

        print(post_data)

def executeCommand(_userId, _interaction, _action):

    #/UserId/Interaction/Action
    userId = _userId
    interaction = _interaction
    action = _action

    player = ""
    for account in accounts:
        if account.data["id"] == userId:
            player = account
            break

    if interaction == "abc":
        pass

    #Commands unabhaengig der interaction
    else:
        if action == "status":
            response = Response("Status ist ok")

        #travel 5:5
        elif action.find("travel", 0, 6) != -1:
            print(action)

            xy = action.split("%20")[1]
            player.data["sector"]["x"] = int(xy.split(":")[0])
            player.data["sector"]["y"] = int(xy.split(":")[1])
            response = Response("Your Action: " + action)
            print(player.data)

        #Kein valider Command
        else:
            response = Response("Command unknwon")

        resJson = json.dumps(response.data)
        return resJson

accounts = [Account()]

httpd = HTTPServer(("localhost", 8080), Serv)
httpd.serve_forever()
