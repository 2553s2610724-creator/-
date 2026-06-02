import streamlit as st
from google import genai

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="고민상담 챗봇",
    page_icon="💬",
    layout="centered"
)

st.title("💬 고민상담 챗봇")
st.caption("당신의 고민을 편하게 이야기해 보세요.")

# ---------------------------
# API 키 불러오기
# ---------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Secrets에 GEMINI_API_KEY가 설정되어 있지 않습니다.")
    st.stop()

# ---------------------------
# Gemini 클라이언트 생성
# ---------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# ---------------------------
# 시스템 프롬프트
# ---------------------------
SYSTEM_PROMPT = """
당신은 따뜻하고 공감 능력이 뛰어난 고민상담 챗봇입니다.

원칙:
1. 사용자의 감정을 존중합니다.
2. 섣부르게 판단하거나 비난하지 않습니다.
3. 공감을 먼저 표현합니다.
4. 현실적이고 구체적인 조언을 제공합니다.
5. 지나치게 장황하지 않게 답변합니다.
6. 정신건강, 법률, 의료 등 전문 영역은 전문가 상담을 권유할 수 있습니다.
"""

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# 기존 대화 표시
# ---------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------
# 사이드바
# ---------------------------
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------
# 사용자 입력
# ---------------------------
user_input = st.chat_input("고민을 입력해 주세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        try:
            # 대화 이력 구성
            conversation = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "상담사"
                conversation += f"{role}: {msg['content']}\n"

            prompt = f"""
{SYSTEM_PROMPT}

아래는 지금까지의 대화입니다.

{conversation}

상담사:
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            error_message = (
                "죄송합니다. 응답을 생성하는 중 오류가 발생했습니다.\n\n"
                f"오류 내용: {str(e)}"
            )

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )
