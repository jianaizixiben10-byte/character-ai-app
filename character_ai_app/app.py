import streamlit as st
from openai import OpenAI

st.title("🐹 オリジナルキャラ生成AI")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

tab1, tab2, tab3 = st.tabs([
    "🐹 プロフィール",
    "✨ キャラ生成",
    "💬 会話"
])

st.sidebar.title("🐹 ちゃむAIメニュー")
st.sidebar.write("できること")
st.sidebar.write("・キャラ生成")
st.sidebar.write("・ちゃむと会話")
st.sidebar.write("・会話履歴")
st.sidebar.write("・会話リセット")
st.sidebar.info("ちゃむは食いしん坊で温厚な男の子です。語尾は〜ちゃむ。")

api_key = st.secrets["OPENAI_API_KEY"]

with tab1:
    st.image("character_ai_app/chamu.png", width=300)
    st.subheader("🐹 ちゃむ")
    st.write("## 🌟 キャラクタープロフィール")
    st.write("名前：ちゃむ")
    st.write("性別：男の子")
    st.write("性格：食いしん坊・温厚")
    st.write("好きなもの：おやつ、野菜")
    st.write("苦手なもの：爪切り")
    st.write("口癖：〜ちゃむ")

with tab2:
    st.write("テーマを入力するとAIがキャラクターを生成します")

    theme = st.text_input(
        "どんなキャラにしたい？",
        key="theme_input"
    )

    if st.button("生成", key="generate_button"):
        if not theme:
            st.warning("キャラテーマを入力してください")
        else:
            client = OpenAI(api_key=api_key)

            prompt = f"""
以下のテーマで、魅力的なオリジナルキャラクターを作成してください。

テーマ：
{theme}

出力内容：
・名前
・年齢
・種族
・見た目
・性格
・一人称
・口調
・好きなもの
・苦手なもの
・趣味
・特技
・弱点
・口癖
・背景ストーリー
・一言セリフ

初心者にも読みやすく、項目ごとに分かりやすく書いてください。
"""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            character = response.choices[0].message.content
            st.session_state["character"] = character

            st.subheader("✨ 生成されたキャラクター")
            st.write(character)

with tab3:
    st.subheader("💬 キャラと会話する")

    user_message = st.text_input(
        "キャラに話しかけてみよう",
        key="chat_input"
    )

    if st.button("会話をリセット", key="reset_chat"):
        st.session_state["chat_history"] = []
        st.success("会話履歴をリセットしました")

    if st.button("話しかける", key="chat_button"):
        if not user_message:
            st.warning("メッセージを入力してください")
        elif "character" not in st.session_state:
            st.warning("先にキャラクターを生成してください")
        else:
            client = OpenAI(api_key=api_key)

            character_setting = st.session_state.get("character", "")

            chat_prompt = f"""
あなたは以下のキャラクターです。

{character_setting}

このキャラクターになりきって返事してください。

必ず語尾に「〜ちゃむ」を自然につけてください。
性格は、食いしん坊で温厚な男の子です。
苦手なものは爪切りです。
"""

            messages = [
                {
                    "role": "system",
                    "content": chat_prompt
                }
            ]

            for chat in st.session_state["chat_history"]:
                messages.append(
                    {
                        "role": "user",
                        "content": chat["user"]
                    }
                )
                messages.append(
                    {
                        "role": "assistant",
                        "content": chat["assistant"]
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )

            reply = response.choices[0].message.content

            st.session_state["chat_history"].append(
                {
                    "user": user_message,
                    "assistant": reply
                }
            )

            st.subheader("💬 キャラの返事")
            st.write(reply)

    st.subheader("📚 会話履歴")

for chat in st.session_state["chat_history"]:
    st.chat_message("user").write(chat["user"])
    st.chat_message("assistant").write(chat["assistant"])