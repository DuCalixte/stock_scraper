#!/usr/bin/python
import os
import posixpath
import urllib
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import sys, getopt
import cgi

ROUTES = (
	['','/app'],
	['/','/app']
	)

class ServerHandler(BaseHTTPRequestHandler):

	
	def translate_path(self, path):
		# """translate path given routes"""
		print path
		# set default root to cwd
		root = os.getcwd()
		print root
		# look up routes and set root directory accordingly
		for pattern, rootdir in ROUTES:
			if path.startswith(pattern):
				# found match!
				path = path[len(pattern):]  # consume path up to pattern len
				root = rootdir
				break
		# normalize path and prepend root directory
		path = path.split('?',1)[0]
		path = path.split('#',1)[0]
		path = posixpath.normpath(urllib.unquote(path))
		words = path.split('/')
		words = filter(None, words)

		path = root
		for word in words:
			drive, word = os.path.splitdrive(word)
			head, word = os.path.split(word)
			if  word in (os.curdir, os.pardir):
				continue

			path = os.path.join(path, word)

		return path


	# Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/app/index.html"
		else:
			self.path = self.translate_path(self.path)

		try:
			# Check the file extension required and set the right mime type
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".json"):
				mimetype='text/json'
				sendReply = True
			if self.path.endswith(".xml"):
				mimetype='text/xml'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/png'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".woff"):
				mimetype='application/font-woff'
				sendReply = True
			if self.path.endswith(".ttf"):
				mimetype='application/font-ttf'
				sendReply = True
			if self.path.endswith(".eot"):
				mimetype='application/vnd.ms-fontobject'
				sendReply = True
			if self.path.endswith(".otf"):
				mimetype='application/font-otf'
				sendReply = True
			if self.path.endswith(".svg"):
				mimetype='image/svg+xml'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True

			if sendReply == True:
				# Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()

			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	# Handler for the POST requests
	def do_POST(self):
		if self.path=="submit" or self.path=="send":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
				environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],}
				)
			# print "Your name is: %s" % form["your_name"].value
			self.send_response(200)
			self.end_headers()
			# self.wfile.write("Thanks %s !" % form["your_name"].value)
			return

def main(argv=None):
	address = '127.0.0.1'
	port = 8000

	if argv is not None:
		try:
			opts, args = getopt.getopt(argv,"hp:a:",["port=","address="])
		except getopt.GetoptError:
			print 'simple_cgi_python_server.py -p <port> -a <address>'

		for opt, arg in opts:
			if opt == '-h':
				print 'simple_cgi_python_server.py -p <port> -a <address>'
			elif opt in ("-p", "--port"):
				try:
					port = int(arg)
				except ValueError:
					print "This port [", arg, "] is incorrect, try a valid integer for port..."
					sys.exit(3)
			elif opt in ("-a", "--address"):
				address = arg

	try:
		# Create a web server and define the handler to manage the incoming request
		server = HTTPServer((address, port), ServerHandler)
		socket_info = server.socket.getsockname()
		print "Serving HTTP on", socket_info[0], "port", socket_info[1], "..."

		# Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()

if __name__ == '__main__':
    main(sys.argv[1:])

