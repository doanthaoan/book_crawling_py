print("Xin chào, đây là chương trình \"Ai là triệu phú\" bản fa-kè")
# Khởi tạo giá trị điểm ban đầu = 0
diem = 0

# Câu hỏi 1
# - In ra màn hình nội dung câu hỏi
print("1. Đâu là thủ đô nước Mỹ?")
print("A: New York")
print("B: Washington DC.")
print("C: London")
print("D: Hà Nội")
# - Cho người dùng nhập đáp án câu hỏi 1 và lưu vào biến dap_an_1
dap_an_1 = input("Câu trả lời của bạn là A, B, C hay D?: ")
# - Kiểm tra và chấm điểm 
if (dap_an_1 == "A") or (dap_an_1 == "C") or (dap_an_1 == "D"):
    thong_bao_1 = "Đáp án câu số 1 của bạn là " + dap_an_1 + ", chưa chính xác."
    diem = diem - 1
elif (dap_an_1 == "B"):
    thong_bao_1 = "Đáp án câu số 1 của bạn là " + dap_an_1 + ", chính xác!"
    diem = diem + 1
else:
    thong_bao_1 = "Bạn chọn đáp án câu số 1 không phải là A, B, C, D. Sai yêu cầu!"
    diem = diem - 1
    


