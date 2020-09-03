import itertools
import math
import time


class ResistanceFinder:
    def __init__(self, resistances):
        # for k=1
        self.resistors1 = {r: "R("+str(r)+")" for r in resistances}
        
        # for k=2
        self.resistors2 = {}
        for r1, r2 in itertools.combinations(resistances, 2):
            r1_ = str(r1)
            r2_ = str(r2)
            # serial
            self.resistors2[r1 + r2] = "S("+r1_+"+"+r2_+")"
            # parallel
            self.resistors2[1/(1/r1 + 1/r2)] = "P("+r1_+"|"+r2_+")"
        
        # for k=3
        self.resistors3 = {}
        for r1, r2, r3 in itertools.combinations(resistances, 3):
            r1_ = str(r1)
            r2_ = str(r2)
            r3_ = str(r3)
            # serial
            self.resistors3[r1 + r2 + r3] = "S("+r1_+"+"+r2_+"+"+r3_+")"
            # parallel
            self.resistors3[1/(1/r1 + 1/r2 + 1/r3)] = "P("+r1_+"|"+r2_+"|"+r3_+")"
        for r1, r2, r3 in itertools.permutations(resistances, 3):
            r1_ = str(r1)
            r2_ = str(r2)
            r3_ = str(r3)
            # P( a | S(b+c) )
            self.resistors3[1/(1/r1 + 1/(r2+r3))] = "P("+r1_+"|S("+r2_+"+"+r3_+"))"
            # S( a + P(b|c) )
            self.resistors3[r1+1/(1/r2 + 1/r3)] = "S("+r1_+"+P("+r2_+"|"+r3_+"))"
        
        # for k=4
        self.resistors4 = {}
        for r1, r2, r3, r4 in itertools.combinations(resistances, 4):
            r1_ = str(r1)
            r2_ = str(r2)
            r3_ = str(r3)
            r4_ = str(r4)
            # serial
            self.resistors4[r1+r2+r3+r4] = "S("+r1_+"+"+r2_+"+"+r3_+"+"+r4_+")"
            # parallel
            self.resistors4[1/(1/r1+1/r2+1/r3+1/r4)] = "P("+r1_+"|"+r2_+"|"+r3_+"|"+r4_+")"
        for r1, r2, r3, r4 in itertools.permutations(resistances, 4):
            r1_ = str(r1)
            r2_ = str(r2)
            r3_ = str(r3)
            r4_ = str(r4)
            
            # S(a+b+c+d)
            # in first loop
            # P(a | S(b+c+d))
            self.resistors4[1/(1/r1 + 1/(r2+r3+r4))] = "P("+r1_+"|"+"S("+r2_+"+"+r3_+"+"+r4_+"))"
            
            # S(a + P(b|S(c+d)))
            self.resistors4[r1 + 1/(1/r2 + 1/(r3+r4))] = "S("+r1_+"+P("+r2_+"|S("+r3_+"+"+r4_+")))"
            # P(a | P(b|S(c+d))) -> P(a | b | S(c+d))
            self.resistors4[1/(1/r1 + 1/r2 + 1/(r3+r4))] = "P("+r1_+"|"+r2_+"|S("+r3_+"+"+r4_+"))"
            
            # S(a +   b+P(c|d))
            self.resistors4[r1 + r2 + 1/(1/r3 + 1/r4)] = "S("+r1_+"+"+r2_+"+P("+r3_+"|"+r4_+"))"
            # P(a | S(b+P(c|d)))
            self.resistors4[1/(1/r1 + 1/(r2 + 1/(1/r3+1/r4)))] = "P("+r1_+"|"+"S("+r2_+"+P("+r3_+"|"+r4_+")))"
            
            # S(a + P(b|c|d))
            self.resistors4[r1 + 1/(1/r2 + 1/r3 + 1/r4)] = "S("+r1_+"+P("+r2_+"|"+r3_+"|"+r4_+"))"
            
            # P(S(a|b) | S(c|d))
            self.resistors4[1/(1/(r1+r2) + 1/(r3+r4))] = "P(S("+r1_+"+"+r2_+")|S("+r3_+"+"+r4_+"))"
            # S(P(a|b) + P(c|d))
            self.resistors4[1/(1/r1 + 1/r2) + 1/(1/r3 + 1/r4)] = "S(P("+r1_+"|"+r2_+"+P("+r3_+"|"+r4_+")))"
            # P( P(a|b) | P(c|d))
            #self.resistors4[1/(1/(1/r1+1/r2) + 1/(1/r3+1/r4))] = "P(P("+r1_+"|"+r2_+")|P("+r3_+"|"+r4_+"))"

            # P( P(a|b) | S(c|d))
            #self.resistors4[1/(1/(1/r1+1/r2) + 1/(r3+r4))] = "P(P("+r1_+"|"+r2_+")|S("+r3_+"+"+r4_+"))"
            
        self.resistors = {1: self.resistors1,
                          2: self.resistors2,
                          3: self.resistors3,
                          4: self.resistors4}
    
    def find(self, r, k):
      try:
          # Das zu k gehörende dict
          resistors = self.resistors[k]
      except KeyError:
          # k ist kein Schlüssel von dict, also ist k nicht richtig
          raise ValueError("Parameter 'k' must be 1, 2, 3 or 4, not "+str(k))
      
      if not resistors:
          # das dict ist leer, weil es nicht genügend Widerstandswerte für k gibt.
          return None
      # Das Schlüssel-Wert-Paar (als Tupel) mit der kleinsten Differenz zu r wird zurückgegeben
      return min(resistors.items(), key=lambda item: abs(r-item[0]))

    def find_best(self, r):
        return min(((k, self.find(r, k)) for k in range(1, 5)),
                   key=lambda result: abs(r-result[1][0]) if result[1] is not None else math.inf)

    def print_results(self, r):
        results = []
        for k in range(1, 5):
            res = self.find(r, k)
            if res is not None:
                results.append((k, res[0], res[1]))
        for k, resistance, diagram in results:
            print("k={k} {r:.4f}Ω Diagramm: {d}".format(k=k, r=resistance, d=diagram))
        best_k, best_r, best_diagram = min(results, key=lambda res: abs(r-res[1]))  # compare resistances
        print("##\nBESTE KOMBINATION: k={k} {r:.4f}Ω (Abweichung ~{diff:.2%}) Diagramm: {d}"
              .format(k=best_k, r=best_r, diff=abs(best_r-r)/r, d=best_diagram))


if __name__ == "__main__":
    with open("widerstaende.txt", "r") as f:
        resistances = tuple(int(r.strip()) for r in f.readlines())
    print("Lade Widerstände... (dauert bei mir weniger als 4 Sekunden)")
    t1 = time.perf_counter()
    finder = ResistanceFinder(resistances)
    t2 = time.perf_counter()

    print("Liste in", t2-t1, "geladen")
    print("Alle Widerstände auf 4 Nachkommastellen gerundet. Werte in Diagrammen in Ohm. ")
    
    for r in (500, 140, 314, 315, 1620, 2719, 4242):
        print("\n############", r, "==", sep="\n")
        finder.print_results(r)
