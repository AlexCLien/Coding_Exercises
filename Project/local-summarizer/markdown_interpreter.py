import markdown

class MarkDownToHTML:
    def __init__(self,input):
        self.input = input

    def build_html(self):
        markdown_text = self.input
        html = markdown.markdown(markdown_text)
        return html
