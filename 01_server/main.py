from http.server import HTTPServer, BaseHTTPRequestHandler
from account import Account
import json
import urllib.parse


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

                reply = executeCommand(
                    post_data["userId"], post_data["interaction"], post_data["action"])
                self.send_response(200, 'Good Stuff')

            else:
                self.send_response(
                    400, 'Bad Request: content type must be valid application/json')
                reply = '400 Bad Request: content type must be valid application/json'
        except:
            self.send_response(500, 'Internal Error: shit broke very hard.')
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
            print(action)

            #  "%20" does not longer exist, as it it is clean json now. JSON does not have this shit anly loger
            # this results in a "list index out of range" error. PLS FIX.
            xy = action.split("%20")[1]
            player.data["sector"]["x"] = int(xy.split(":")[0])
            player.data["sector"]["y"] = int(xy.split(":")[1])
            response = Response("Your Action: " + action)
            print(player.data)

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
