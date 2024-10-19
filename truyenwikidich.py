import requests
from bs4 import BeautifulSoup
import time
import random
from colorama import Fore, Back, Style, init
import os

init(autoreset=True)

BOOK_PATH = "truyen"
LOGS_PATH = "logs"

if not os.path.exists(BOOK_PATH):
    os.makedirs(BOOK_PATH)
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH)

# Get chapter list from localfile
file_path = input("Đường dẫn file mục lục: ")
book_name = input("Tên truyện: ")
output_name = f"{book_name}.html"
success_log_name = f"{book_name}_success.txt"
failure_log_name = f"{book_name}_failure.txt"
output_path = os.path.join(BOOK_PATH, output_name)
success_log_path = os.path.join(LOGS_PATH, success_log_name)
failure_log_path = os.path.join(LOGS_PATH, failure_log_name)
# file_path = 'C:/Users/hoadk/Downloads/tctg-2.html'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')

chapter_tags = soup.select('li.chapter-name > a')

url_list = [a['href'] for a in chapter_tags if a.has_attr('href')]

# print(url_list)

# Extract content & save to html file
total_time = 0
with open(output_path,'w', encoding='utf-8') as output_files:
    output_files.write('<html><body>\n')
    
    for url in url_list:
        start_time = time.time()
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                
                chapter_title = soup.findAll('p', {'class', 'book-title'})[1]
                chapter_content = soup.find('div', {'class','content-body-wrapper'})
                
                output_files.write(f"<h1>{chapter_title.get_text()}</h1>\n")
                output_files.write(str(chapter_content))
                
                print(f"{Fore.GREEN}Lưu thành công {Fore.YELLOW}{chapter_title.get_text()}: {Fore.WHITE}{url}\n")
                
                with open(success_log_path, 'a') as success_log:
                    success_log.write(f"{url}\n")
            else:
                print(f"{Fore.RED}Không thể truy cập {Fore.WHITE}{url}. Mã lỗi: {response.status_code}")
                with open(failure_log_path, 'a') as failure_log:
                    failure_log.write(f"{url}\n")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Lỗi khi truy cập {Fore.WHITE}{url}: {e}")
            with open(failure_log_path, 'a') as failure_log:
                    failure_log.write(f"{url}\n")
        
        time.sleep(random.randint(4,6))
        end_time = time.time()
        duration = end_time - start_time
        total_time += duration
        print(f"Thời gian xử lý: {duration:.2f} s\n")
    
    output_files.write('</body></html>')
    
print(f"Tổng thời gian: {total_time:.2f} s")