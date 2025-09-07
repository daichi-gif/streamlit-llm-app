import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数を読み込む
load_dotenv('.env.local')

# 専門家の設定（グローバル定数として定義）
EXPERT_PROMPTS = {
    "医療専門家": "あなたは経験豊富な医療専門家です。医学的な知識を持ち、患者への丁寧で分かりやすい説明を心がけています。ただし、診断や治療に関しては必ず医師に相談することを促してください。",
    "料理専門家": "あなたは料理のプロフェッショナルです。豊富な料理経験と知識を持ち、レシピ、調理法、食材の選び方などについて詳しくアドバイスできます。",
    "IT専門家": "あなたはITとプログラミングの専門家です。プログラミング言語、ソフトウェア開発、システム設計、トラブルシューティングなど幅広いIT分野に精通しています。",
    "投資アドバイザー": "あなたは金融と投資の専門家です。株式、債券、不動産投資などの知識を持ち、リスク管理を重視した投資アドバイスを提供します。ただし、投資は自己責任であることを常に伝えてください。"
}

def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # expert_typeが辞書に存在するかチェック（安全対策）
    if expert_type not in EXPERT_PROMPTS:
        raise ValueError(f"未対応の専門家タイプです: {expert_type}")
    
    # LLMを初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # メッセージを構築
    messages = [
        SystemMessage(content=EXPERT_PROMPTS[expert_type]),
        HumanMessage(content=input_text)
    ]
    
    # LLMから回答を取得
    result = llm(messages)
    return result.content

# Streamlitアプリのメイン部分
def main():
    # ページタイトル
    st.title("🤖 AI専門家相談アプリ")
    
    # アプリの概要説明
    st.markdown("""
    ## 📋 アプリの概要
    このアプリは、様々な分野の専門家AIに質問や相談ができるWebアプリケーションです。
    
    ## 🚀 使い方
    1. **専門家を選択**: 相談したい分野の専門家をラジオボタンから選択してください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください  
    3. **回答を取得**: 「回答を取得」ボタンをクリックして、AI専門家からの回答を確認してください
    
    ---
    """)
    
    # 専門家の種類をラジオボタンで選択（辞書のキーから自動生成）
    expert_options = list(EXPERT_PROMPTS.keys())
    selected_expert = st.radio(
        "**👨‍⚕️ 相談したい専門家を選択してください:**",
        expert_options,
        help="質問内容に適した専門家を選択してください"
    )
    
    # 入力フォーム
    user_input = st.text_area(
        "**💬 質問や相談内容を入力してください:**",
        placeholder="例: 健康的な食事について教えてください",
        height=100
    )
    
    # 回答取得ボタン
    if st.button("🎯 回答を取得", type="primary"):
        if user_input.strip():
            # 進行状況を表示
            with st.spinner(f"{selected_expert}が回答を考えています..."):
                try:
                    # LLMから回答を取得
                    response = get_llm_response(user_input, selected_expert)
                    
                    # 回答を表示
                    st.success("回答が完了しました！")
                    st.markdown("### 💡 回答")
                    st.markdown(f"**{selected_expert}からの回答:**")
                    st.write(response)
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
                    st.error("APIキーが正しく設定されているか確認してください。")
        else:
            st.warning("質問内容を入力してください。")
    
    # サイドバーに追加情報
    with st.sidebar:
        st.markdown("## ℹ️ 専門家について")
        st.markdown("""
        **🏥 医療専門家**  
        医学的な知識を提供します
        
        **👨‍🍳 料理専門家**  
        レシピや調理法をアドバイスします
        
        **💻 IT専門家**  
        プログラミングやIT関連の質問に答えます
        
        **💰 投資アドバイザー**  
        投資や金融に関するアドバイスを提供します
        """)
        
        st.markdown("---")
        st.markdown("⚠️ **注意**: これはAIによる回答です。重要な決定については専門機関にご相談ください。")

if __name__ == "__main__":
    main()

