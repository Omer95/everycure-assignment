from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re

def extract_text_and_normalize(element):
   # Extract text from line and split it with new lines
   line_texts = element.get_text().split('\n')
   norm_text = ''
   for line_text in line_texts:
       line_text=line_text.strip()
       # empty strings after striping convert to newline character
       if not line_text:
           line_text = '\n'
       else:
           line_text = re.sub('\s+', ' ', line_text)
           # if the last character is not a letter or number,
                                # add newline character to a line
           if not re.search('[\w\d\,\-]', line_text[-1]):
               line_text+='\n'
           else:
               line_text+=' '
       # concatenate into single string
       norm_text+=line_text
   return norm_text

def process_page(extracted_page):
   content = []


   # Get a sorted list of elements based on 
                # their Y-coordinate in reverse order
   elements = [element for element in extracted_page._objs]
   elements.sort(key=lambda a: a.y1, reverse=True)


   for i, element in enumerate(elements):
       # Extract text if the element is a text container 
       # and text extraction is enabled
       if isinstance(element, LTTextContainer):
           line_text = extract_text_and_normalize(element)
           content.append(line_text)

   # Combine and clean up the extracted content
   content = re.sub('\n+', '\n', ''.join(content))
   return content

def process_document(pdf_path, page_ids=None):
   extracted_pages = extract_pages(pdf_path, page_numbers=page_ids)
   page2content = {}

   # Process each extracted page
   for extracted_page in extracted_pages:
       page_id = extracted_page.pageid
       content = process_page(extracted_page)
       page2content[page_id] = content

   return page2content