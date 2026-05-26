import streamlit as st
st.title('사과는 맛있다')
st.write('바이브코딩 재미있다!!')
import streamlit as st
from datetime import date

st.set_page_config(page_title="하루 일기", page_icon="📔")

st.title("📔 하루 일기 앱")

today = date.today()

st.write(f"오늘 날짜: {today}")

diary = st.text_area(
    "오늘 있었던 일을 적어보세요",
    height=200
)

if st.button("저장하기"):
    if diary.strip() == "":
        st.warning("일기를 입력해주세요!")
    else:
        filename = f"diary_{today}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(diary)

        st.success("일기가 저장되었습니다!")
