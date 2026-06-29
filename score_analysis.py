import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
from PIL import Image

st.title("Phân tích dữ liệu điểm số học sinh")
st.divider()

#I. User upload file xlsx. Kiểm tra user đã upload chưa

uploaded_file = st.file_uploader("Chọn file Excel (có cột 'Điểm số')", type=["xlsx"])
if uploaded_file:
    st.write(f"File của bạn là: {uploaded_file.name}") # thông báo tên file đã upload
else:
    st.write(f"Bạn chưa up file")          # Hiện thông báo khi chưa upload

#II.Các hàm xử lý dữ liệu

# 1.Hàm tính điểm trung bình
def calculate_average(scores):
    return sum(scores)/len(scores)

# 2. Hàm phân loại điểm số - Hàm chia điểm số thành 5 nhóm và đếm số lượng học sinh trong mỗi nhóm
def percentage_distribution (scores):
    bins = {"90-100": 0, "80-89": 0 , "70-79":0 , "60-69": 0 , "<60":0 }
    for score in scores:
        if score >= 90:
            bins["90-100"] +=1
        elif score >=80:
            bins["80-89"] += 1
        elif score >=70:
            bins["70-79"] += 1
        elif score >=60:
            bins["60-69"] += 1
        else:
            bins["<60"] += 1
    return bins

#III. Đọc flie excel và hiển thị trung bình
#a. Đọc File
def main():
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        scores = df["Điểm số"].dropna().astype(float).tolist()  #b.Xử lý danh sách điểm số
        if scores:
            st.write("Tổng số học sinh:", len(scores))
            st.write("Điểm trung bình:", round(calculate_average(scores),2)) #c.Hiển thị các điểm số
        #b. Phân loại điểm
            dist = percentage_distribution(scores)
            labels = list(dist.keys())
            values = list(dist.values())
        #c. Vẽ biểu đổ
            fig, ax = plt.subplots(figsize = (8, 8))
            ax.pie(
                values,
                labels = labels,
                autopct = "%1.1f%%",
                textprops = {"fontsize": 22,"family": "Times"},
                colors =['#335c67', '#fff3b0', '#e09f3e', '#9e2a2b', '#540b0e'],
            )
            ax.axis("equal")
            plt.tight_layout(pad = 0.1)
        #lưu biểu đồ bằng hình ảnh
            buf = io.BytesIO()
            fig.savefig(buf, format = "png", dpi = 300)
            buf.seek(0)
            st.markdown("Biểu đồ phân bố điểm.")
            img = Image.open(buf)

            col1, col2, col3 = st.columns([1,2,1])  # Tạo 3 cột, cột giữa rộng hơn

            with col2:
                st.image (img, width = 300)  # hiện thị biểu đồ ở cột giữa
                st.markdown("<p style='text-align: center;'>Biểu đồ phân bố điểm</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
        




