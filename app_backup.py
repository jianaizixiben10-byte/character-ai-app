import streamlit as st
from openai import OpenAI

st.title("🐹 オリジナルキャラ生成AI")

st.write("テーマを入力するとAIがキャラクターを生成します")

api_key = st.text_input(
    "OpenAI APIキーを入力",
    type="password",
    key="api_key_input"
)

theme = st.text_input(
    "どんなキャラにしたい？",
    key="theme_input"
)

if st.button("生成", key="generate_button"):

    if not api_key:
        st.warning("APIキーを入力してください")

    elif not theme:
        st.warning("キャラテーマを入力してください")

    else:

        client = OpenAI(api_key=api_key)

        prompt = f"""
        以下のテーマで、
        魅力的なオリジナルキャラクターを作成してください。

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

        初心者にも読みやすく、
        項目ごとに分かりやすく書いてください。
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

        st.subheader("✨ 生成されたキャラクター")

        st.write(character)
        