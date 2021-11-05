import sys
from collections import deque


def main():
    input_pth = sys.argv[1]
    
    with open(input_pth, "r") as input_file:
        # parse input
        inp = deque(input_file.readlines())
        
        case_count = int(inp.popleft())
        cases = []
        for _ in range(case_count):
            # append (synonym record, queries)
            cases.append( (pop_lines(inp), pop_lines(inp)) )
        
        all_answeres = []
        for synonyms, queries in cases:
            all_answeres.extend(solve_case(synonyms, queries))
        
        with open("output.txt", "w") as output_file:
            output_file.write("\n".join(all_answeres) + "\n")
    
    return


def pop_lines(deq):
    n = int(deq.popleft())
    records = []
    for _ in range(n):
        [a, b] = deq.popleft().strip().split(" ")
        records.append((a.lower(), b.lower()))
        
    return records


def solve_case(synonyms, queries):
    # g = build_graph(synonyms)
    # print(g)
    s = Synonyms(synonyms)
    
    answers = []
    for w1, w2 in queries:
        answers.append(
            "synonyms" if s.query(w1, w2) else "different"
            )

    return answers


class Synonyms:
    def __init__(self, arr):
        self.db = dict()
        self.counter = 0
        for w1, w2 in arr:
            self.add(w1, w2)
    
    
    def add(self, w1, w2):
        if w1 not in self.db and w2 not in self.db:
            self.db[w1] = self.counter
            self.db[w2] = self.counter
            self.counter += 1
        
        elif w1 not in self.db:
            self.db[w1] = self.db[w2]
            
        elif w2 not in self.db:
            self.db[w2] = self.db[w1]
        
        else:
            # worst case scenario
            old_gid = self.db[w2]
            new_gid = self.db[w1]
            for k in self.db.keys():
                if self.db[k] == old_gid:
                    self.db[k] = new_gid


    def query(self, w1, w2):
        if w1 == w2:
            return True
        return w1 in self.db and w2 in self.db and self.db[w1] == self.db[w2]        


# abandoned naive and overcomplicated approach:

# def build_graph(synonyms):
#     graph = dict()
    
#     for w1, w2 in synonyms:
#         old = None
#         if w1 not in graph and w2 not in graph:
#             graph[w1] = {w1, w2}
#             graph[w2] = {w2, w1}
            
#         if w1 not in graph:
#             graph[w1] = set()
#             graph[w2].add(w1)
#             for w in graph[w2]:
#                 # ensure transitivity
#                 graph[w].add(w1)
            
        
#         # ensure symetry
#         if w2 not in graph:
#             graph[w2] = set()
#         graph[w2].add(w1)
        
#         graph[w1] = graph[w1].union(graph[w2])
#         graph[w2] = graph[w2].union(graph[w1])
    
#     return graph


# def test_synonyms(graph, w1, w2):
#     return w1 == w2 or (w2 in graph and w1 in graph[w2])



if __name__ == '__main__':
    main()

