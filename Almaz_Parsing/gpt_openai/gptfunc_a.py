import tiktoken
import matplotlib.pyplot as plt

class gptfunc_a_class:
    def num_tokens_from_string(self, string: str, encoding_name: str= "cl100k_base") -> int:
      """Возвращает количество токенов в строке"""
      encoding = tiktoken.get_encoding(encoding_name)
      num_tokens = len(encoding.encode(string))
      return num_tokens
    def hist(self, fragments):
      fragment_token_counts = [self.num_tokens_from_string(fragment.page_content, "cl100k_base") for fragment in fragments]
      plt.hist(fragment_token_counts, bins=20, alpha=0.5, label='Fragments')
      plt.title('Distribution of Fragment Token Counts')
      plt.xlabel('Token Count')
      plt.ylabel('Frequency')
      plt.show()

    def split_text(self, docs):
      from langchain.text_splitter import MarkdownHeaderTextSplitter
      headers_to_split_on = [
          ("#", "H1"),
          ("##", "H2"),
          ("###", "H3"),
      ]
      markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
      fragments =[]
      for text in docs:
          fragments.extend( markdown_splitter.split_text(text))
      return fragments
    
