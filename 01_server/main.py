from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class Response():
    data = {
        "message" : "",
        "interaction" : ""
    }

    def __init__(self, _message, _interaction):
        self.data["message"] = _message
        self.data["interaction"] = _interaction

class Serv(SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    #komplexe ai #machine learning
    def do_GET(self):
        splittedPath = self.path.split("/")

        #/UserId/Interaction/Action
        userId = splittedPath[-3]
        interaction = splittedPath[-2]
        action = splittedPath[-1]

        print(splittedPath)

        if interaction == "sector":
            pass


        #Commands unabhaengig der interaction
        else:
            if action == "status":
                response = Response("Status ist ok", "")

            elif action.find("travel", 0, 6) != -1:
                response = Response("Your Action: " + action, "")

            #Kein valider Command
            else:
                response = Response("Command unknwon", "")


        resJson = json.dumps(response.data)
        self.send_response(200)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(resJson, "utf-8"))

httpd = HTTPServer(("localhost", 8080), Serv)
httpd.serve_forever()
