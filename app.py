import streamlit as st
st.title('사과는 맛있다')
st.write('바이브코딩 재미있다!!')
import streamlit as st
import random

st.set_page_config(page_title="고민상담 앱", page_icon="💬")

st.title("💬 고민상담 앱")

st.write("고민을 입력하면 간단한 위로와 조언을 해드립니다.")

worries = st.text_area(
    "당신의 고민을 적어주세요",
    height=200
)

answers = [
    "너무 혼자 끌어안지 않아도 괜찮아요.",
    "천천히 하나씩 해결해보세요.",
    "지금까지도 잘 버텨왔어요.",
    "잠시 쉬어가는 것도 중요합니다.",
    "당신의 감정은 충분히 소중합니다.",
    "완벽하지 않아도 괜찮아요.",
]

if st.button("상담받기"):
    if worries.strip() == "":
        st.warning("고민을 입력해주세요!")
    else:
        result = random.choice(answers)

        st.subheader("🫶 상담 결과")
        st.success(result)
