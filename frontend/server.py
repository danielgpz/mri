from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

def page_not_found():
    f = open('./404.htm', 'r')
    html = f.readlines()
    f.close()
    return html

def search_results(jsons: list, page: int = 0):
    f = open('./result.htm', 'r')
    html = f.readlines()
    f.close()

    pages = (len(jsons) + 9) // 10
    if page < pages:
        pos = -1
        for i in range(len(html)):
            for j in i.split():
                if '@results' in j:
                    pos = i
                    break
        jsons = jsons[page*10:]
        r = []
        for i in jsons[:10]:
            f = open(i, 'r')
            json_obj = json.load(i)
            i.close()
            title = json_obj['title']
            # author = json_obj['author']
            content = json_obj['text']
            if len(content) > 100:
                content = content[0:100] + '...'
            r.append('        <div class="serp__web">')
            r.append('          <span class="serp__label">Web Results</span>')
            r.append('          <div class="serp__result">')
            r.append('            <a href="##" target="_blank">')
            r.append(f'              <div class="serp__title">{title}</div>')
            r.append('            </a>')
            # <span class="serp__match">bb</span>
            r.append(f'            <span class="serp__description"> {content} </span>')
            r.append('          </div>')
            r.append('        </div>')
        html = html[:pos] + r + html[pos:]

        pos = -1
        for i in range(len(html)):
            for j in i.split():
                if '@pagination' in j:
                    pos = i
                    break
        p = []
        p.append('        <div class="serp__pagination">')
        p.append('          <ul>')
        p.append('            <li><a class="serp__disabled"></a></li>')
        for i in range(pages):
            if i == page:
                p.append(f'            <li class="serp__pagination-active"><a href="/page/{i}"></a></li>')
            else:
                p.append(f'            <li><a href="/page/{i}"></a></li>')
        p.append('          </ul>')
        p.append('        </div>')
        html = html[:pos] + p + html[pos:]
        return html
    
    if pages == 0 and page == 0:
        pos = -1
        for i in range(len(html)):
            for j in i.split():
                if '@noresults' in j:
                    pos = i
                    break
        nr = []
        nr.append('        <div class="serp__no-results">')
        nr.append('          <p><strong>No search results were found for &raquo;labore et dolore&laquo;</strong></p>')
        nr.append('          <p>Suggestions:</p>')
        nr.append('          <ul>')
        nr.append('            <li>Check that all words are spelled correctly.</li>')
        nr.append('            <li>Try different search terms.</li>')
        nr.append('            <li>Try a more general search.</li>')
        nr.append('            <li>Try fewer search terms.</li>')
        nr.append('          </ul>')
        nr.append('        </div>')
        html = html[:pos] + nr + html[pos:]
        return html

    return page_not_found()


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # if self.path.startswith('/page/')

        # self.wfile.write(bytes())
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

hostName = "localhost"
serverPort = 8080

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.") 
