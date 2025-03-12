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

    img_format = img.format.lower() # PNG인지 JPEG인지 확인
    
    quality = 95 # 초기 품질 설정

    if img_format == "png":
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format="PNG", optimize=True) # PNG 최적화
        
    else: # JPEG인 경우
        img_byte_arr = io.BytesIO()
        while True:
            img_byte_arr.seek(0)
            resized_img.save(img_byte_arr, format='JPEG', quality=quality)
            size_kb = len(img_byte_arr.getvalue()) / 1024

            if size_kb <= max_size_kb or quality <= 10:
                break

            quality -= 5

    return img_byte_arr.getvalue()

st.title("사진 크기를 한번에 줄이는 프로그램")

uploaded_files = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button("사진 크기 줄이기"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for uploaded_file in uploaded_files:
                processed_image = resize_and_compress_image(uploaded_file)
                zipf.writestr(f"{uploaded_file.name}", processed_image)

        zip_data = zip_buffer.getvalue()
        st.download_button(
            label="처리된 이미지 파일들 다운로드",
            data=zip_data,
            file_name="사진파일.zip",
            mime="application/zip"
        )
        st.success("이미지 처리 다운로드 완료!")
