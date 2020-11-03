'''
:: Process ::
1. Gets the URL from the main.py
2. Gets the cleaned text from the HTML webpage by passing the URL to fetchWebpage.py
3. Preprocessing of the text is done here, and it returnes the text back to main.py
'''

from fetchWikipage import FetchWikipage
import re

# TODO :: apply advance text preprocessing techniques to extract high quality data from a
# wiki page/any data source.
# TODO :: improve text cleaning and preprocessing technique !!
class TextPreprocessing:

    @staticmethod
    def process(url:str=None, saveHTML2text:bool=False) -> str:
        '''General text cleaning and preprocessing methods are applied here'''
        webpage_obj = FetchWikipage()
        text = webpage_obj.generateHTML2text(url)

        text.strip()
        text = re.sub(r"<!--(.|\s|\n)*?-->", '', text) # Remove comments
        text = re.sub(r'\n+', ' ', text)     # replace multiple newlines to single line

        text = re.sub(r'\[.*?\]', '', text)  # eg: [string] => ''
        text = re.sub(r'\]+', '', text)      # eg: string] => string
        text = re.sub(r'\[+', '', text)      # eg: [string => string

        text = re.sub(r'\(.*?\)', '', text)  # eg: (string) => ''
        text = re.sub(r'\)+', '', text)      # eg: string) => string
        text = re.sub(r'\(+', '', text)      # eg: (string => string

        text = re.sub(r'\|.*?\|', '', text)  # eg: |string| => ''
        text = re.sub(r'\|+', '', text)      # eg: string| => string

        text = re.sub(r'\.+', '.', text)     # eg: ... => .
        text = re.sub(r'\-+', ' ', text)     # eg: --- => ' '
        text = re.sub(r'\*+', '', text)      # eg: * => ''

        text = re.sub(r'"', '', text)        # eg: "string" => string
        text = re.sub(r"'", '', text)        # eg: 'string' => string
        text = re.sub(r'\s+\,', ',', text)   # eg: string , => string,
        text = re.sub(r'\s+\.', '.', text)   # eg: string . => string.
        text = re.sub(r'\;', '', text)       # eg: string; => string

        print("[INFO] Cleaning & Preprocessing of HTML is done.")
        if(saveHTML2text):
            with open("./textual_data/html_2_text.txt", 'w', encoding='utf8') as f:
                f.write(text)
            print("[INFO] HTML 2 Text data has been added to './textual_data/html_2_text.txt'")
        return text


if __name__ == "__main__":
    preprocessed_text = TextPreprocessing.process("https://en.wikipedia.org/wiki/Albert_Einstein", False)
    print(preprocessed_text)