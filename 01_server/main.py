from http.server import HTTPServer, BaseHTTPRequestHandler
from classesLibrary import Account, Ship
import json


hostName = "localhost"
serverPort = 8080


class Response():
    data = {
        "message": "",
        "interaction": ""
    }

    def __init__(self, _message, _interaction=""):
        self.data["message"] = _message
        self.data["interaction"] = _interaction


class Serv(BaseHTTPRequestHandler):
    def send_success(self):
        self.send_response(200)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        pass

    def do_POST(self):

        content_type = self.headers['content-type']

        try:
            if content_type == 'application/json':
                content_length = int(self.headers.get('content-length', 0))
                post_data = json.loads(self.rfile.read(
                    content_length).decode("utf-8"))

                print(post_data);

                reply = executeCommand(
                    post_data["userId"], post_data["interaction"], post_data["action"])
                self.send_response(200, 'Good Stuff')

            else:
                self.send_response(
                    400, 'Bad Request: content type must be valid application/json')
                reply = '400 Bad Request: content type must be valid application/json'
        except:
            self.send_response(500, 'Internal Error: shit broke very hard.') #code is killing me softly xD
            reply = "Error"
        finally:
            self.do_OPTIONS()
            self.wfile.write(bytes(reply, "utf-8"))


def executeCommand(_userId, _interaction, _action):

    # /UserId/Interaction/Action
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

    # Commands unabhaengig der interaction
    else:
        if action == "status":
            response = Response("Status ist ok")

        # travel 5:5
        elif action.find("travel", 0, 6) != -1:

            # this results in a "list index out of range" error. PLS FIX. <-- I LOVE IT
            # >> tried to catch any unexpected input
            # >> we can now handle lots of separator-characters :/-_.;¦|,
            xy = action.split(" ")[1]
            separator = ""

            #looping for x characters through characters > this is anything but nicely readable code
            #searching for a valid seperator character to split x and y coordinates
            for char in ":/-_.;¦|,":
                for _char in xy:
                    if char == _char:
                        separator = char
                        break
                if separator != "":
                    break

            if separator != "" and len(xy.split(separator)) == 2:
                _x = xy.split(separator)[0]
                _y = xy.split(separator)[1]
                response = Response("You reach sector " + _x + ", " + _y)
                #changing game state > seems to wirk fine
                player.data["sector"]["x"] = _x
                player.data["sector"]["y"] = _y
            else:
                response = Response("Command unknwon")

        # Kein valider Command
        else:
            response = Response("Command unknwon")

        resJson = json.dumps(response.data)
        return resJson


accounts = [Account()]


# Server start and stop functionality, with some console output.

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), Serv)
    print("Server started @ http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
