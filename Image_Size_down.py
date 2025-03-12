import streamlit as st
from PIL import Image
import io
import zipfile

def compress_image(image, max_size_kb=300):
    img = Image.open(image)
    quality = 95  # 초기 품질 설정
    img_byte_arr = io.BytesIO()

    while True:
        img_byte_arr.seek(0)  # 스트림 위치 초기화
        img.save(img_byte_arr, format='JPEG', quality=quality)
        size_kb = len(img_byte_arr.getvalue()) / 1024
        
        if size_kb <= max_size_kb or quality <= 10:  # 목표 크기 달성 또는 최소 품질 도달 시 종료
            break
        
        quality -= 5  # 품질 감소
    
    return img_byte_arr.getvalue()

st.title("이미지 파일 용량 300KB 미만으로 일괄 압축 후 ZIP 다운로드")

uploaded_files = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if st.button("이미지 압축 및 ZIP 다운로드"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for uploaded_file in uploaded_files:
                compressed_image = compress_image(uploaded_file)
                zipf.writestr(f"compressed_{uploaded_file.name}", compressed_image)

        zip_data = zip_buffer.getvalue()
        st.download_button(
            label="압축된 이미지 ZIP 파일 다운로드",
            data=zip_data,
            file_name="compressed_images.zip",
            mime="application/zip"
        )
        st.success("이미지 압축 및 ZIP 생성 완료!")
