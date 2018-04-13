from http.server import BaseHTTPRequestHandler, HTTPServer


'''
this won't work
...looking into asyncio http server

'''


# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.get_data()
        return bytes(self.content, 'UTF-8')

    def get_data(self, geojson):
        self.lat = -22.1831903
        self.lon = 119.2604059
        self.geojson = '{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (self.lat,self.lon)
        self.content = self.geojson

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

 
class run():

    def __init__(self,):
        self.server = {'Status':'',
                       'Response':'',
                       'IP':'',
                       'Port':'',
                       }
        self.server['Status'] = "Starting"
        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, RequestHandler)
        self.server['Status'] = "Running"
        httpd.serve_forever()
 
if __name__ == '__main__':
    
    run()
