import http.server
import socketserver
import os
import mimetypes

PORT = 3000

mimetypes.init()
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Keep local preview in sync while static experience is iterated
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def send_error_404(self):
        not_found_file = os.path.join(os.getcwd(), '404.html')
        if os.path.isfile(not_found_file):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            with open(not_found_file, 'rb') as f:
                content = f.read()
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File not found")

    def do_GET(self):
        # Handle /_next/image queries
        if self.path.startswith('/_next/image'):
            import urllib.parse
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if 'url' in params:
                img_url = params['url'][0]
                if img_url.startswith('http'):
                    self.send_response(302)
                    self.send_header('Location', img_url)
                    self.end_headers()
                    return
                elif img_url.startswith('/images/'):
                    self.path = img_url
                    return super().do_GET()

        clean_url = self.path.split('?')[0].split('#')[0]

        # Exact file match on disk
        local_path = self.translate_path(clean_url)
        if os.path.isfile(local_path):
            return super().do_GET()

        # Handle privacy and disclaimer (styled reference 404)
        norm_path = clean_url.strip('/')
        if norm_path in ['privacy', 'disclaimer']:
            target_html = os.path.join(os.getcwd(), f"{norm_path}.html")
            if os.path.isfile(target_html):
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                with open(target_html, 'rb') as f:
                    content = f.read()
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                return self.send_error_404()

        # Clean URLs without trailing slash: e.g. /countries -> countries.html or countries/index.html
        if norm_path:
            cand_html = os.path.join(os.getcwd(), (norm_path + '.html').replace('/', os.sep))
            cand_idx = os.path.join(os.getcwd(), norm_path.replace('/', os.sep), 'index.html')

            if os.path.isfile(cand_html):
                self.path = '/' + norm_path + '.html'
                return super().do_GET()
            elif os.path.isfile(cand_idx):
                self.path = '/' + norm_path + '/index.html'
                return super().do_GET()
        elif clean_url in ['/', '']:
            if os.path.isfile(os.path.join(os.getcwd(), 'index.html')):
                self.path = '/index.html'
                return super().do_GET()

        # Route not found -> branded 404 page
        return self.send_error_404()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    with ThreadedTCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Server serving clean URLs and branded 404 on port {PORT} (Multi-threaded)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
