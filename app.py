
import streamlit as st
import pandas as pd
import datetime
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image
import io

st.title("WORK TALK 위험성평가 참여 시스템")

# 본인 인증
st.header("본인 인증")
name = st.text_input("이름을 입력하세요")
phone = st.text_input("휴대폰 번호를 입력하세요 (010부터)")

# 사진 업로드
st.header("사진 업로드")
uploaded_file = st.file_uploader("위험작업 사진을 업로드하세요", type=['jpg', 'jpeg', 'png'])

# 사진 미리보기
if uploaded_file is not None:
    st.image(uploaded_file, caption="업로드한 사진 미리보기", use_column_width=True)

# 질문
st.header("위험성평가 질문")
place = st.text_input("0. 이 작업장소는 어디인가요?")
work = st.text_input("1. 어떤 작업을 하고 있나요?")
danger_reason = st.text_input("2. 이 작업은 왜 위험하다고 생각하나요?")

freq = st.radio("3. 이 작업은 얼마나 자주 하나요?", 
                ["연 1-2회", "반기 1-2회", "월 2-3회", "주 1회 이상", "매일"])

risk = st.radio("4. 이 작업은 얼마나 위험하다고 생각하나요?", 
                ["약간의 위험", "조금 위험", "위험", "매우 위험"])

improvement = st.text_area("5. 이 작업을 더 안전하게 하기 위한 개선 아이디어가 있다면 적어주세요 (선택사항)")

# 제출 버튼
if st.button("제출하기"):
    if not name or not phone or not uploaded_file:
        st.error("이름, 휴대폰번호, 사진은 필수입니다!")
    else:
        st.success("제출이 완료되었습니다! 다운로드 버튼이 활성화 됩니다.")

        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"위험성평가_{name}_{now}.xlsx"

        # 엑셀 생성 (가로 방향)
        wb = Workbook()
        ws = wb.active
        ws.title = "위험성평가 결과"

        # 첫 번째 행에 질문들
        questions = ["이름", "휴대폰 번호", "작업장소", "작업내용", "위험이유", "작업빈도", "위험정도", "개선아이디어"]
        ws.append(questions)

        # 두 번째 행에 답변들
        answers = [name, phone, place, work, danger_reason, freq, risk, improvement]
        ws.append(answers)

        # 사진 삽입
        img = Image.open(uploaded_file)
        img.thumbnail((150, 150))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img_for_excel = XLImage(img_byte_arr)
        ws.add_image(img_for_excel, 'I2')  # I2 셀에 사진 삽입

        # 파일 저장
        wb.save(file_name)

        # 파일 다운로드 버튼
        with open(file_name, "rb") as f:
            st.download_button(
                label="📥 엑셀 파일 다운로드",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
