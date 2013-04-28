# coding: utf-8
'''
Created on 27. apr. 2013

@author: H�kon
'''
import json;
import random;

class Rater(object):
    
    _players = {};
    
    _played = []
    
    start_rating = 1500;
    k = 24;
    f = 400;
    
    def __init__(self):
        pass;
    
    def add(self, strPlayer):
        self._players[strPlayer] = self.start_rating;
        
    def match(self, a, b, res):
        
        if not self.has_been_played(a, b):
            self._played.append([a,b]) #list for json saving
        
        a_score = 0.0;
        b_score = 0.0;
        if res == "A":
            a_score = 1.0;
        elif res == "B":
            b_score = 1.0;
        elif res == "DRAW":
            a_score = 0.5;
            b_score = 0.5;
        else:
            raise Exception("res variable must be A, B or DRAW.")
        diff = self._players[b] - self._players[a];
        
        ea = 1/(1+10**(diff/self.f)) 
        eb = 1/(1+10**(-diff/self.f)) 
        self._players[a] = int(self._players[a] + self.k*(a_score - ea));
        self._players[b] = int(self._players[b] + self.k*(b_score - eb));
        
    def has_been_played(self,a,b):
        return [a,b] in self._played or [b,a] in self._played
           
    def get_results(self):
        lst = []
        for key in self._players:
            lst.append((self._players[key], key));
        lst.sort(reverse=True);
        return lst;
    
    def get_random_match(self):
        return random.sample(self._players.keys(), 2)
    
    def load(self, file):
        with open(file, 'r') as infile:
            o = json.load(infile)
            self._players = o['players'];
            self._played = o['played'];
    
    def save(self, file):
        o = {};
        o['players'] = self._players;
        o['played'] = self._played;
        
        with open(file, 'w') as outfile:
            json.dump(o, outfile)
            
    def print_results(self):
        res = self.get_results();
        for elem in res:
            print "%s: %s" % (elem[1], elem[0])
            

if __name__ == "__main__":
    r = Rater();
    r.load("3klasse.json")
    while True:
        r.print_results()
        match = r.get_random_match();
        print "1: %s, 2: %s, 3: Uavgjort, 4: Avslutt og lagre" % (match[0], match[1])
        input = raw_input("Valg: ")
        if input == "1":
            r.match(match[0], match[1], "A"); 
        elif input == "2":
            r.match(match[0], match[1], "B");
        elif input == "3":
            r.match(match[0], match[1], "DRAW");
        elif input == "4":
            r.save("3klasse.json")
            break
        else:
            print "Ugyldig input"
        print input


    
    
