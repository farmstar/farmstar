from http.server import BaseHTTPRequestHandler, HTTPServer
import fs_nmea

server = {'Status':'',
          'Response':'',
          'IP':'',
          'Port':'',
          }


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
        lat = nmea.GGA['Latitude']
        lon = nmea.GGA['Longitude']
        content = '{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (lat,lon)
        return bytes(content, 'UTF-8')

    

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)
    
 
def run():
  server['Status'] = "Starting"
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, RequestHandler)
  server['Status'] = "Running"
  httpd.serve_forever()
 
 
run()
