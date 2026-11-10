
import streamlit as st

from demo import answer_demo
from rag import answer_question


st.set_page_config(
    page_title="BuildingBot",
    page_icon="🏢",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        direction: rtl;
    }

    .stChatMessage {
        direction: rtl;
        text-align: right;
    }

    [data-testid="stChatInput"] {
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏢 BuildingBot")
st.write("העוזר החכם של ועד הבית")

mode = st.radio(
    "בחרי מצב הפעלה:",
    ["הדגמה חינמית", "RAG אמיתי - OpenAI"],
)

if mode == "הדגמה חינמית":
    st.warning(
        "מצב הדגמה: תשובות מוגדרות מראש "
        "על בסיס מסמכי הדוגמה. "
        "לא מתבצע חיפוש וקטורי או שימוש במודל AI."
    )
else:
    st.info(
        "מצב RAG: חיפוש במסמכים באמצעות "
        "LlamaIndex ו-ChromaDB, "
        "ויצירת תשובות באמצעות OpenAI."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.get("previous_mode") != mode:
    st.session_state.messages = []
    st.session_state.previous_mode = mode

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "מה תרצו לדעת על הבניין?"
)

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("מעבד את השאלה..."):
            try:
                if mode == "הדגמה חינמית":
                    answer, sources = answer_demo(question)
                else:
                    answer, sources = answer_question(question)

                st.markdown(answer)

                saved_answer = answer

                if sources:
                    source_text = ", ".join(sources)
                    st.caption("מקורות: " + source_text)
                    saved_answer += "\n\nמקורות: " + source_text

            except Exception as error:
                saved_answer = (
                    "אירעה שגיאה בעת עיבוד השאלה."
                )
                st.error(saved_answer)
                st.code(str(error))

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": saved_answer,
        }
    )
