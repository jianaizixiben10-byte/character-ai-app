import streamlit as st
from openai import OpenAI
import base64
import os
from datetime import datetime

def make_image_prompt(character):
    prompt = f"""
anime style original character illustration.

Use the following character profile to create the image:

{character}

high quality,
beautiful lighting,
full body,
clean background,
anime style,
no text,
no watermark,
no logo
"""

    return prompt

def generate_character_image(prompt, api_key):
    client = OpenAI(api_key=api_key)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json

    image_bytes = base64.b64decode(image_base64)

    return image_bytes

def save_image(image_bytes, character_name="character"):
    os.makedirs("generated_images", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_images/{character_name}_{timestamp}.png"

    with open(filename, "wb") as f:
        f.write(image_bytes)

    return filename

st.set_page_config(
    page_title="ちゃむAI",
    page_icon="🐹",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background-color: #FFF8F0;
}

h1 {
    color: #5B3A29;
    text-align: center;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    padding: 10px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

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
    st.image("chamu.png", width=300)
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

            image_prompt = make_image_prompt(character)
            st.session_state["image_prompt"] = image_prompt

if "image_prompt" in st.session_state:
    st.subheader("🎨 画像生成メニュー")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("画像プロンプトを表示", key="show_image_prompt"):
            st.write(st.session_state["image_prompt"])

    with col2:
        if st.button("画像を生成", key="generate_image"):
            with st.spinner("画像を生成中..."):
                image_bytes = generate_character_image(
                    st.session_state["image_prompt"],
                    api_key
                )

            st.session_state["character_image"] = image_bytes
            st.success("画像を生成しました")

if "character_image" in st.session_state:
    st.subheader("🖼️ 生成されたキャラクター画像")

    st.image(
        st.session_state["character_image"],
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("画像を保存", key="save_image"):
            saved_path = save_image(
                st.session_state["character_image"]
            )

            st.success(f"画像を保存しました: {saved_path}")

    with col2:
        if st.button("画像を再生成", key="regenerate_image"):
            with st.spinner("画像を再生成中..."):
                image_bytes = generate_character_image(
                    st.session_state["image_prompt"],
                    api_key
                )

            st.session_state["character_image"] = image_bytes
            st.success("画像を再生成しました")
            
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