import streamlit as st
from utils import save_chat, read_chat_history
from search_tool import SearchTool
from prompts import RESEARCH_SUMMARY_PROMPT, CHAT_WITH_HISTORY_PROMPT

def run_app(route_request, get_models):
    st.set_page_config(page_title="AI Research Agent", layout="wide")
    
    # --- CUSTOM CSS ---
    st.markdown("""
        <style>
        .research-box {
            background-color: #1A2634;
            border-left: 5px solid #0078D4;
            padding: 15px;
            border-radius: 8px;
            color: #FFFFFF;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💬 AI Research Chat Agent")

    # --- INITIALIZE SESSION STATE ---
    if "search_agent" not in st.session_state: 
        st.session_state.search_agent = SearchTool()
    if "messages" not in st.session_state: 
        st.session_state.messages = []
    if "search_results" not in st.session_state: 
        st.session_state.search_results = []

    # --- SIDEBAR: SETTINGS ---
    st.sidebar.header("⚙️ Settings")
    backend = st.sidebar.radio("Backend", ["Local", "API"])
    models = get_models()
    selected_model = st.sidebar.selectbox("Model", models) if models else None

    # --- SIDEBAR: DATA MANAGEMENT ---
    st.sidebar.markdown("---")
    st.sidebar.header("📁 Data Management")
    
    doc_option = st.sidebar.selectbox("Memory Source", ["None", "chat_history.txt"])

    if st.sidebar.button("Load Memory"):
        if doc_option == "chat_history.txt":
            with st.spinner("Injecting history..."):
                file_content = read_chat_history()
                if "ERROR" in file_content:
                    st.sidebar.error(file_content)
                else:
                  st.session_state.messages.append({
                    "role": "system",
                    "content": f"""
                ### PERSISTENT RESEARCH MEMORY ###
                You MUST treat everything below as your ONLY source of truth.

                {file_content}

                ### END MEMORY ###
                """,
                    "is_research": True,
                    "display_url": "💾 Local History"
                })
                st.rerun()

    if st.sidebar.button("Save Current Chat"):
        if st.session_state.messages:
            path = save_chat(st.session_state.messages)
            st.sidebar.success(f"Saved to {path}")

    # --- THE CLEAR BUTTON (FIXED INDENTATION) ---
    if st.sidebar.button("Clear Chat Window"):
        st.session_state.messages = []
        st.session_state.search_results = []
        st.rerun()

    # --- SIDEBAR: SEARCH ---
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Research Menu")
    query = st.sidebar.text_input("Enter Topic")
    
    if st.sidebar.button("Run Web Search"):
        with st.sidebar:
            with st.spinner("Browsing..."):
                st.session_state.search_results = st.session_state.search_agent.search(query)

    for i, res in enumerate(st.session_state.search_results):
        with st.sidebar.expander(f"📄 {res['title'][:30]}..."):
            if st.button("Summarize Page", key=f"side_sum_{i}"):
                with st.spinner("Scraping..."):
                    raw_text = st.session_state.search_agent.scrape(res['url'])
                    final_prompt = RESEARCH_SUMMARY_PROMPT.format(url=res['url'], context=raw_text)
                    st.session_state.messages.append({
                        "role": "user", 
                        "content": final_prompt,
                        "is_research": True,
                        "display_url": res['url']
                    })
                st.rerun()

    # --- MAIN CHAT DISPLAY ---
    for msg in st.session_state.messages:
        if msg.get("is_research"):
            st.markdown(f"""
                <div class="research-box">
                    <b>🔍 Research Injected</b><br>
                    <span style="color: #60A5FA;">Source: {msg.get('display_url')}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # --- CHAT INPUT & RESPONSE TRIGGER ---
    if user_input := st.chat_input("Ask a follow-up..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            try:
                response_generator = route_request(
                    st.session_state.messages, 
                    selected_model, 
                    backend
                )
                full_response = st.write_stream(response_generator)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"AI Error: {str(e)}")