class Extractor:
    def __init__(self, file):
        self.adjectives = []
        with open(file, "r") as f:
            for line in f:
                self.adjectives.append(line.strip())
    
    def extract(self, sentence):
        lines = list()
        parts = sentence.split()
        for i in range(len(parts) - 1):
            if parts[i] in self.adjectives:
                lines.append(parts[i] + " " + parts[i + 1])
        return lines