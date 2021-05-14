from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from main import SearchEngine
import os, sys
import shutil

def load_html(file: str):
    f = open(os.path.join(os.getcwd(), 'frontend', file), 'r')
    html = f.readlines()
    f.close()
    return html

def search_results(query: str, se: SearchEngine, page: int = 0, select: int = -1):
    jsons = se.query(query)
    
    html = load_html('result.htm')

    def find_pos(patt: str):
        for i in range(len(html)):
            for j in html[i].split():
                if patt in j:
                    return i + 1
        assert 0

    pos = find_pos('@query')
    html = html[:pos] + [f'              <input name="q" type="search" value="{query}" autofocus\n'] + html[pos:]

    pages = (len(jsons) + 9) // 10
    if page < pages:
        pos = find_pos('@results')
        jsons = jsons[page*10:]
        r = []
        s = []
        for i in jsons[:10]:
            f = open(os.path.join(os.getcwd(), 'docs', se.name + i + '.json'), 'r')
            json_obj = json.load(f)
            f.close()
            title = json_obj['title']
            author = json_obj['author']
            content = json_obj['text']
            preview = content
            if len(preview) > 300:
                preview = preview[0:300] + '...'
            r.append('        <div class="serp__web">')
            r.append('          <span class="serp__label">Web Results</span>')
            r.append('          <div class="serp__result">')
            r.append(f'            <a href="?q={query}&p={page}&s={i}">')
            r.append(f'              <div class="serp__title">{title}</div>')
            r.append('            </a>')
            # <span class="serp__match">bb</span>
            r.append(f'            <span class="serp__description"> {preview} </span>')
            r.append('          </div>')
            r.append('        </div>')
        
            if i == str(select) or select == -1:
                select = i
                s.append(f'            <div class="serp__headline">{author}</div>')
                s.append('            <div class="serp__wiki">')
                s.append(f'              <h2>{title}</h2>')
                s.append(f'              <p>{content}</p>')
                s.append('            </div>')

        html = html[:pos] + [i + '\n' for i in r] + html[pos:]

        pos = find_pos('@sidebar')
        html = html[:pos] + [i + '\n' for i in s] + html[pos:]

        pos = find_pos('@pagination')
        p = []
        p.append('        <div class="serp__pagination">')
        p.append('          <ul>')
        p.append('            <li><a class="serp__disabled"></a></li>')
        for i in range(pages):
            if i == page:
                p.append(f'            <li class="serp__pagination-active"><a href="?q={query}&p={i}"></a></li>')
            else:
                p.append(f'            <li><a href="?q={query}&p={i}"></a></li>')
        p.append('          </ul>')
        p.append('        </div>')
        html = html[:pos] + [i + '\n' for i in p] + html[pos:]

        return html

    if pages == 0 and page == 0:
        pos = find_pos('@noresults')
        nr = []
        nr.append('        <div class="serp__no-results">')
        nr.append(f'          <p><strong>No search results were found for &raquo;{query}&laquo;</strong></p>')
        nr.append('          <p>Suggestions:</p>')
        nr.append('          <ul>')
        nr.append('            <li>Check that all words are spelled correctly.</li>')
        nr.append('            <li>Try different search terms.</li>')
        nr.append('            <li>Try a more general search.</li>')
        nr.append('            <li>Try fewer search terms.</li>')
        nr.append('          </ul>')
        nr.append('        </div>')
        html = html[:pos] + [i + '\n' for i in nr] + html[pos:]
        return html

    return load_html('404.html')


# hostName = "localhost"
hostName = sys.argv[1]
# serverPort = 8080
serverPort = int(sys.argv[2])
# vectors_path = './docs/CISI.vectors.json'
vectors_path = sys.argv[3]
# keywords_path = './docs/CISI.keywords.json'
keywords_path = sys.argv[4]

class MyServer(BaseHTTPRequestHandler):  
    def do_GET(self):
        if self.path.endswith(".css"):
            f = open(os.path.join(os.getcwd(), 'frontend') + self.path, 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        
        if self.path.endswith(".jpg") or self.path.endswith(".png"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg' if self.path.endswith(".jpg") else 'image/png')
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'frontend') + self.path, 'rb') as content:
                shutil.copyfileobj(content, self.wfile)
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if not self.path or self.path == '/':
            html = load_html('index.htm')
            for l in html:
                self.wfile.write(bytes(l, 'utf-8'))
            return

        try:
            p = urlparse(f'http://{hostName}:{serverPort}' + self.path)
            q = parse_qs(p.query)
            if 'q' in q:
                page = 0
                if 'p' in q:
                    page = int(q['p'][0])
                select = -1
                if 's' in q:
                    select = int(q['s'][0])
                html = search_results(q['q'][0], self.se, page, select)
                # f = open('ht.html', 'w')
                # f.writelines(html)
                # f.close()
                for l in html:
                    self.wfile.write(bytes(l, 'utf-8'))
                return
        except Exception:
            pass

        html = load_html('404.html')
        for l in html:
            self.wfile.write(bytes(l, 'utf-8'))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    webServer.RequestHandlerClass.se = SearchEngine(vectors_path, keywords_path)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.") 
