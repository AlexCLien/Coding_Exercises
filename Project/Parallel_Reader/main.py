class Text:
    def __init__(self, title, author,language, text):
        self.title = title
        self.author = author
        self.language = language
        self.text = text

    def print_text(self):
        for element in self.text:
            print(element)

    def get_sentence(self,index):
        return self.text[index - 1]

class ParallelText:
    def __init__(self, text_a, text_b):
        self.text_a = text_a
        self.text_b = text_b
        self.alignment = {}

    def align(self):
        for index_a, index_b in zip(
            range(len(self.text_a.text)),
            range(len(self.text_b.text))
        ):
            key = index_a
            value = index_b
            self.alignment[key] = value  
        return self.alignment


english = Text("Example", "Author", "English",[
    "Sentence one.",
    "Sentence two.",
    "Sentence three."
])

spanish = Text(
    "Ejemplo",
    "Author",
    "Spanish",
    ["Oración uno.", "Oración dos.","Oración thres"]
)

mandarin = Text(
    "例子",
    "Author",
    "Mandarin",
    ["第一句。", "第二句。"]
)
english.print_text()
print(english.get_sentence(2))

english_spanish = ParallelText(english,spanish)
english_spanish.align()
print(english_spanish.alignment)