class TextChunker:
    def __init__(self, text, chunk_size):
        self.text = text
        self.chunk_size = chunk_size

    def chunk_text(self):
        chunks = []
        words = self.text.split()
        for start in range(0, len(words), self.chunk_size):
            stop = start + self.chunk_size
            chunk = words[start:stop]
            chunk_string = " ".join(chunk)
            chunks.append(chunk_string)
        return chunks
