#!/usr/bin/env python3

class aho_corasick:
    def __init__(self, keywords: dict):
        self.go = []
        self.fail = []
        self.endpos = []
        self.keywordsSize = len(keywords)
        
        def add_node():
            pos = len(self.go)
            self.go.append({})
            self.fail.append(0)
            self.endpos.append([])
            return pos

        add_node()
        for word in keywords:
            e = 0
            for c in word:
                if c not in self.go[e]:
                    nn = add_node()
                    self.go[e][c] = nn
                e = self.go[e][c]
            self.endpos[e].append(keywords[word])
        
        que = []
        for c in self.go[0]:
            que.append(self.go[0][c])

        pos = 0
        while pos < len(que):
            e = que[pos]
            pos += 1
            f = self.fail[e]
            for c in self.go[e]:
                self.fail[self.go[e][c]] = self.find(f, c)
                que.append(self.go[e][c])
    
    def find(self, e: int, c):
        while e and c not in self.go[e]:
            e = self.fail[e]
        if c in self.go[e]:
            e = self.go[e][c]
        return e
    
    def match(self, text: str):
        vector = [0] * self.keywordsSize
        e = 0
        for c in text:
            e = self.find(e, c)
            ee = e
            while ee:
                for i in self.endpos[ee]:
                    vector[i] += 1
                ee = self.fail[ee]
        return vector
