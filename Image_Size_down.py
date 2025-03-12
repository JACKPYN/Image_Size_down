import streamlit as st
from PIL import Image
import io
import zipfile

def resize_and_compress_image(image, resize_percent=0.7, max_size_kb=300):
    img = Image.open(image)
    original_width, original_height = img.size
    new_width = int(original_width * resize_percent)
    new_height = int(original_height * resize_percent)
    resized_img = img.resize((new_width, new_height))

    quality = 95  # 초기 품질 설정
    img_byte_arr = io.BytesIO()

    while True:
        img_byte_arr.seek(0)
        resized_img.save(img_byte_arr, format='JPEG', quality=quality)
        size_kb = len(img_byte_arr.getvalue()) / 1024

        if size_kb <= max_size_kb or quality <= 10:
            break

        quality -= 5

    return img_byte_arr.getvalue()

st.title("이미지 해상도 70%로 축소하는 프로그램")

uploaded_files = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button("이미지 처리 및 ZIP 다운로드"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for uploaded_file in uploaded_files:
                processed_image = resize_and_compress_image(uploaded_file)
                zipf.writestr(f"processed_{uploaded_file.name}", processed_image)

        zip_data = zip_buffer.getvalue()
        st.download_button(
            label="처리된 이미지 ZIP 파일 다운로드",
            data=zip_data,
            file_name="processed_images.zip",
            mime="application/zip"
        )
        st.success("이미지 처리 및 ZIP 생성 완료!")
