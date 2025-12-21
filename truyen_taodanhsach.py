import pandas as pd
import os
from pathlib import Path
from unidecode import unidecode
import re

def clean_title(title):
    """Chuyển đổi tên truyện thành dạng SEO"""
    if pd.isna(title):
        return ""
    
    title = str(title)
    title = unidecode(title)
    title = title.lower()
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'[\s]+', '-', title)
    title = re.sub(r'-+', '-', title)
    title = title.strip('-')
    return title if title else ""

def format_stt(stt):
    """Định dạng STT thành 3 chữ số"""
    if pd.isna(stt):
        return "000"
    
    stt = str(stt).strip()
    return f"{int(stt):03d}" if stt.isdigit() else stt

def create_html_file(folder_path, file_name, original_title):
    """Tạo file HTML với nội dung cơ bản"""
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <title>{original_title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>{original_title}</h1>
    <!-- Nội dung sẽ được cập nhật sau -->
</body>
</html>''')
    return file_path

def main():
    # Thiết lập đường dẫn
    folder_path = 'book_source'
    input_file = os.path.join(folder_path, 'danhsach.xlsx')
    output_file = os.path.join(folder_path, 'danh_sach_truyen_seo.xlsx')
    
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    # Đọc file gốc
    df = pd.read_excel(input_file)
    
    # Đọc hoặc khởi tạo file output với đầy đủ cột
    if os.path.exists(output_file):
        df_combined = pd.read_excel(output_file)
        
        # Tìm các bản ghi mới
        new_records = df[~df['Tên'].isin(df_combined['Tên'])].copy()
    else:
        # Khởi tạo file mới với đầy đủ cột
        df_combined = df.copy()
        df_combined['Tên SEO cơ bản'] = ''
        df_combined['Tên SEO đầy đủ'] = ''
        df_combined['Đã tạo HTML'] = False
        df_combined['Lý do'] = ''
        new_records = df_combined.copy()
    
    # Xử lý các bản ghi mới
    if not new_records.empty:
        print(f"Phát hiện {len(new_records)} bản ghi mới cần xử lý")
        
        # Tạo tên SEO cho các bản ghi mới
        new_records['Tên SEO cơ bản'] = new_records['Tên'].apply(clean_title)
        new_records['Tên SEO đầy đủ'] = new_records.apply(
            lambda row: f"{format_stt(row['STT'])}-{row['Tên SEO cơ bản']}.html", 
            axis=1
        )
        new_records['Đã tạo HTML'] = False
        new_records['Lý do'] = ''
        
        # Kết hợp với dữ liệu cũ
        df_combined = pd.concat([df_combined, new_records], ignore_index=True)
    else:
        print("Không có bản ghi mới nào cần xử lý")
    
    # Tạo file HTML cho các bản ghi chưa được tạo
    new_files_created = 0
    existing_files = 0
    
    for index, row in df_combined.iterrows():
        if pd.notna(row['Tên SEO đầy đủ']) and not row['Đã tạo HTML']:
            basic_seo_name = f"{row['Tên SEO cơ bản']}.html"
            basic_file_path = os.path.join(folder_path, basic_seo_name)
            full_file_path = os.path.join(folder_path, row['Tên SEO đầy đủ'])
            
            if os.path.exists(full_file_path):
                df_combined.at[index, 'Lý do'] = 'File đã tồn tại (cùng STT)'
                existing_files += 1
                print(f"⚠️ File đã tồn tại: {row['Tên SEO đầy đủ']}")
            elif os.path.exists(basic_file_path):
                df_combined.at[index, 'Lý do'] = 'File đã tồn tại (tên cơ bản)'
                existing_files += 1
                print(f"⚠️ File đã tồn tại (tên cơ bản): {basic_seo_name}")
            else:
                try:
                    create_html_file(folder_path, row['Tên SEO đầy đủ'], row['Tên'])
                    df_combined.at[index, 'Đã tạo HTML'] = True
                    df_combined.at[index, 'Lý do'] = 'Tạo mới thành công'
                    new_files_created += 1
                    print(f"✅ Đã tạo file: {row['Tên SEO đầy đủ']}")
                except Exception as e:
                    df_combined.at[index, 'Lý do'] = f'Lỗi khi tạo: {str(e)}'
                    print(f"❌ Lỗi khi tạo file {row['Tên SEO đầy đủ']}: {str(e)}")
    
    # Lưu kết quả
    df_combined.to_excel(output_file, index=False)
    
    print(f"\n📊 Kết quả:")
    print(f"- Tổng số truyện: {len(df_combined)}")
    print(f"- File HTML mới: {new_files_created}")
    print(f"- File đã tồn tại: {existing_files}")
    print(f"- File đã lưu: {output_file}")

if __name__ == "__main__":
    main()