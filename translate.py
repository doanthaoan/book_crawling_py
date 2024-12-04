import os
import re
import requests
import time
import random
from docx import Document
from colorama import Fore, Back, Style, init
init(autoreset=True)

API_ENDPOINT = "https://dichtienghoa.com/transtext"

def append_to_docx(docx_filename, chapter_content):
    # Kiểm tra xem file đã tồn tại chưa
    if os.path.exists(docx_filename):
        doc = Document(docx_filename)  # Mở file nếu tồn tại
    else:
        doc = Document()  # Tạo tài liệu mới nếu chưa có file
    
    # doc.add_heading(clean_text(chapter_title.get_text()), level=1)
    
    # Thêm nội dung mới vào tài liệu
    lines = chapter_content.split('\n', 1)
    title = lines[0]  # The first line is the title
    content = lines[1] if len(lines) > 1 else ""
    doc.add_heading(title, level=1)
    # for paragraph in chapter_content:
    for paragraph in content.split('\n'):
        doc.add_paragraph((paragraph))
    
    # Lưu lại tài liệu ngay lập tức
    try:    
        doc.save(docx_filename)
        print(f"{Fore.GREEN}Lưu thành công DOCX {Fore.YELLOW}{title}")
    except PermissionError:
        print(f"{Fore.RED}Lỗi: Không thể ghi file '{docx_filename}' do quyền hạn hoặc file đang được sử dụng.")
    except FileNotFoundError:
        print(f"{Fore.RED}Lỗi: Thư mục đích không tồn tại. Kiểm tra lại đường dẫn lưu file.")
    except Exception as e:
        print(f"{Fore.RED}Đã có lỗi xảy ra khi lưu file: {e}")
        
# file_content = open("D:\\末世大佬穿到古代被流放.txt","r",  encoding='utf-8').read()
file_content = open("D:\\a.txt","r",  encoding='utf-8').read()
# Use regular expression to split the file into chapters
# Match pattern: chapter numbers at the start of a line
chapters = re.split(r"(?=\b\d+\.\s第\d+章)", file_content)

# Remove any empty strings and strip extra whitespace
chapters = [chapter.strip() for chapter in chapters if chapter.strip()]

# print(chapters[1])
for chapter_content in chapters:
    # chapter_content = open("D:\\a.txt", "r", encoding='utf-8')
    
    data = {
        't': chapter_content,
        'tt': "vi"
    }
    try:
        r = requests.post(url=API_ENDPOINT, data=data)

        if (r.status_code == 200):
            result = r.json()
            append_to_docx("D:\\dich.docx", result["data"])
        else:
            print(f"{Fore.RED}API dịch trả về lỗi. Mã lỗi: {r.status_code}")
        time.sleep(random.randint(2,5))
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Lỗi khi truy cập gọi api dịch: {e}")
