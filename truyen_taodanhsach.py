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
    return f"{title}.html" if title else ""

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
    
    # Đảm bảo thư mục tồn tại
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    # Đọc file gốc
    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {input_file}")
        return
    
    # Kiểm tra và khởi tạo cột mới nếu cần
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)
        
        # Thêm cột 'Lý do' nếu chưa có
        if 'Lý do' not in existing_df.columns:
            existing_df['Lý do'] = ''
            
        # Tìm các bản ghi mới chưa có trong file output
        new_records = df[~df['Tên'].isin(existing_df['Tên'])]
        
        if not new_records.empty:
            print(f"Phát hiện {len(new_records)} bản ghi mới cần xử lý")
            # Tạo tên SEO cho các bản ghi mới
            new_records['Tên SEO'] = new_records['Tên'].apply(clean_title)
            new_records['Đã tạo HTML'] = False
            new_records['Lý do'] = ''
            
            # Kết hợp với dữ liệu cũ
            df_combined = pd.concat([existing_df, new_records], ignore_index=True)
        else:
            print("Không có bản ghi mới nào cần xử lý")
            df_combined = existing_df
    else:
        print("Tạo file mới từ danh sách gốc")
        df['Tên SEO'] = df['Tên'].apply(clean_title)
        df['Đã tạo HTML'] = False
        df['Lý do'] = ''
        df_combined = df
    
    # Tạo các file HTML mới và xử lý file tồn tại
    new_files_created = 0
    existing_files = 0
    
    for index, row in df_combined.iterrows():
        if pd.notna(row['Tên SEO']) and not row['Đã tạo HTML']:
            file_path = os.path.join(folder_path, row['Tên SEO'])
            
            if os.path.exists(file_path):
                # File đã tồn tại
                df_combined.at[index, 'Lý do'] = 'File đã tồn tại'
                existing_files += 1
                print(f"⚠️ File đã tồn tại: {row['Tên SEO']}")
            else:
                try:
                    create_html_file(folder_path, row['Tên SEO'], row['Tên'])
                    df_combined.at[index, 'Đã tạo HTML'] = True
                    df_combined.at[index, 'Lý do'] = 'Tạo mới thành công'
                    new_files_created += 1
                    print(f"✅ Đã tạo file: {row['Tên SEO']}")
                except Exception as e:
                    df_combined.at[index, 'Lý do'] = f'Lỗi khi tạo: {str(e)}'
                    print(f"❌ Lỗi khi tạo file {row['Tên SEO']}: {str(e)}")
    
    # Lưu file danh sách đã cập nhật
    df_combined.to_excel(output_file, index=False)
    
    print(f"\n📊 Kết quả:")
    print(f"- Tổng số truyện trong danh sách: {len(df_combined)}")
    print(f"- Số file HTML mới được tạo: {new_files_created}")
    print(f"- Số file đã tồn tại: {existing_files}")
    print(f"- File danh sách đã được cập nhật tại: {output_file}")

if __name__ == "__main__":
    main()