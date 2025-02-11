import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f"Received GET request for: {self.path}")  # Debug output

        # Handle the root path and serve the HTML page (index.html)
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            try:
                with open("index.html", "rb") as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found: index.html not found')
        else:
            # Handle 404 for unrecognized GET requests
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        # Handle the /search POST request
        if self.path == '/search':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # Parse the incoming JSON data
                data = json.loads(post_data)

                # Process the data
                result = search_patches(data)

                # Send response with status code 200 (OK)
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(result.encode('utf-8'))  # Send the result as bytes

            except json.JSONDecodeError:
                # Handle JSON parsing errors
                self.send_response(400)  # Bad Request
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'There was a problem with parsing the JSON data')

        else:
            # Handle 404 for other paths
            self.send_response(404)  # Not Found
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')


def search_patches(data):
    """Simulate searching for patches in a git repository."""
    # IMPORTANT! Updates the paths to the Linux and QEMU repositories
    repos = ['/path/to/linux', '/path/to/qemu']
    total_patches = ""
    patches_amount = 0
    upstream_action = data["upstream_action"]
    mail = data["mail"]

    for repo in repos:
        os.chdir(repo)
        result = subprocess.run(['git', 'log', f'--grep={upstream_action}.*{mail}', '--pretty=format:%H %s'], capture_output=True, text=True)
        if result.stdout:
            commits = result.stdout.strip().split('\n')
            for commit in commits:
                hash_commit, title = commit.split(' ', 1)  # Separates hash and title
                labels = extract_labels(hash_commit, repo)
                total_patches += f"Title: {title}\n{labels}\n\n"
                patches_amount += 1
        else:
            total_patches += f"No patches found in {repo}.\n"

    return f"Total patches found: {patches_amount}\n\n" + total_patches

def extract_labels(commit_hash, repo):
    """Extract labels (Tested-by, Reported-by, etc.) from a specific commit."""
    os.chdir(repo)
    result = subprocess.run(['git', 'show', commit_hash, '--pretty=format:%B'], capture_output=True, text=True)

    labels = {}
    if result.stdout:
        for line in result.stdout.splitlines():
            if line.startswith('Tested-by:'):
                labels['Tested-by'] = line
            elif line.startswith('Reported-by:'):
                labels['Reported-by'] = line
            elif line.startswith('Signed-off-by:'):
                labels['Signed-off-by'] = line

    return "\n".join(labels.values())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running at http://localhost:{port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
