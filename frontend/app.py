import streamlit as st
import requests
from streamlit.components.v1 import html as components_html

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Task Manager",
    layout="wide",
)

# --- CSS STYLING ---
st.markdown("""
    <style>
        /* Modern gradient background */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Main container with glassmorphism effect */
        .main > div {
            max-width: 1000px;
            padding-left: 50px;
            padding-right: 50px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            margin: 2rem auto;
        }

        /* Full height layout */
        .block-container {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Tabs styling with gradient */
        .stTabs {
            position: sticky;
            top: 0;
            z-index: 100;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: white;
            color: #667eea;
        }

        /* Chat wrapper with proper flex layout */
        .chat-wrapper {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 200px);
            overflow: hidden;
        }

        /* Scrollable chat messages area */
        .chat-scroll {
            flex: 1;
            overflow-y: auto;
            padding: 1rem 0;
            margin-bottom: 1rem;
            max-height: calc(100vh - 300px);
        }

        .chat-input {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 1rem 0;
            border-top: 2px solid #667eea;
            z-index: 50;
        }

        /* Style adjustments for better spacing */
        .stChatInput {
            margin: 0 !important;
        }
        
        /* Chat input field styling */
        .stChatInput > div > div > input {
            border: 2px solid #667eea;
            border-radius: 10px;
        }
        
        .stChatInput > div > div > input:focus {
            border-color: #764ba2;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        /* Custom scrollbar for chat area */
        .chat-scroll::-webkit-scrollbar {
            width: 8px;
        }

        .chat-scroll::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }

        .chat-scroll::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }

        .chat-scroll::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        /* Ensure message spacing */
        .stChatMessage {
            margin-bottom: 1rem;
            border-radius: 10px;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: white;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Success/Error/Info messages */
        .stAlert {
            border-radius: 10px;
            border-left: 4px solid;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONSTANTS ---
BASE_URL = "http://localhost:8000"
TASK_MANAGER_ENDPOINT = f"{BASE_URL}/walker/task_manager"
GET_ALL_TASKS_ENDPOINT = f"{BASE_URL}/walker/get_all_tasks"
REQUEST_TIMEOUT = 30  # seconds

# --- SESSION STATE INIT ---
if 'session_id' not in st.session_state:
    st.session_state.session_id = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'backend_error' not in st.session_state:
    st.session_state.backend_error = False

with st.sidebar:
    st.title("⚙️ Session Management")
    
    # Backend status indicator
    st.markdown("---")
    if st.session_state.backend_error:
        st.error("⚠️ Backend Disconnected")
        st.caption(f"Cannot reach {BASE_URL}")
    else:
        st.success("✅ Backend Connected")
    
    st.markdown("---")
    
    if st.button("🔄 Start New Session"):
        # Just reset the virtual session and chat history
        st.session_state.session_id = ""
        st.session_state.chat_history = []
        st.session_state.backend_error = False
        st.success("Session reset successfully!")
        st.rerun()

# --- TITLE ---
st.title("🤖 Task Manager")

# --- TABS ---
tab1, tab2 = st.tabs(["💬 Chat", "📅 Scheduled Tasks"])

# ========================
#       CHAT INTERFACE
# ========================
with tab1:
    # Do not call backend until user sends first message

    # Create the main chat wrapper
    chat_container = st.container()
    with chat_container:
        # Scrollable messages area
        messages_container = st.container()
        with messages_container:
            st.markdown('<div id="chat-scroll" class="chat-scroll">', unsafe_allow_html=True)
            # Display all chat messages
            for entry in st.session_state.chat_history:
                with st.chat_message(entry["role"]):
                    st.markdown(entry["content"], unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Auto-scroll to newest message
        if st.session_state.chat_history:
            components_html(
                """
                <script>
                  setTimeout(() => {
                    const el = window.parent.document.getElementById('chat-scroll');
                    if (el) { 
                      el.scrollTop = el.scrollHeight; 
                    }
                  }, 100);
                </script>
                """,
                height=0,
            )

    # Fixed typing bar at bottom (outside the scrollable area)
    input_container = st.container()
    with input_container:
        st.markdown('<div class="chat-input">', unsafe_allow_html=True)
        prompt = st.chat_input("Ask me anything...")
        st.markdown("</div>", unsafe_allow_html=True)

    # Handle new messages
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        # If no session_id, create session with first message
        if not st.session_state.session_id:
            payload = {"utterance": prompt, "session_id": ""}
        else:
            payload = {"utterance": prompt, "session_id": st.session_state.session_id}
        
        with st.spinner("🤔 Thinking..."):
            try:
                res = requests.post(
                    TASK_MANAGER_ENDPOINT, 
                    json=payload, 
                    timeout=REQUEST_TIMEOUT
                )
                
                if res.status_code == 200:
                    try:
                        data = res.json()
                        reports = data.get("reports", [])
                        
                        if reports and len(reports) > 0:
                            report = reports[0]
                            message = report.get("response", "")
                            session_id = report.get("session_id", "")
                            
                            if message:
                                st.session_state.session_id = session_id
                                st.session_state.chat_history.append({
                                    "role": "assistant", 
                                    "content": message
                                })
                                st.session_state.backend_error = False
                            else:
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": "⚠️ I received an empty response. Please try again."
                                })
                        else:
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": "⚠️ No response from the assistant. Please check the backend."
                            })
                            
                    except ValueError as e:
                        error_msg = f"❌ Error parsing response: Invalid JSON format. {str(e)}"
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": error_msg
                        })
                        st.error(error_msg)
                        
                elif res.status_code == 404:
                    error_msg = "❌ Backend endpoint not found. Is the backend running correctly?"
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    st.session_state.backend_error = True
                    st.error(error_msg)
                    
                elif res.status_code == 500:
                    error_msg = "❌ Backend server error. Please check the backend logs."
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    st.error(error_msg)
                    
                else:
                    error_msg = f"❌ Unexpected error: HTTP {res.status_code}"
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    st.error(error_msg)
                    
            except requests.exceptions.Timeout:
                error_msg = f"⏱️ Request timed out after {REQUEST_TIMEOUT} seconds. The backend may be overloaded."
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.session_state.backend_error = True
                st.error(error_msg)
                
            except requests.exceptions.ConnectionError:
                error_msg = f"❌ Cannot connect to backend at {BASE_URL}. Make sure the backend is running:\n\n`jac serve backend/main.jac`"
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.session_state.backend_error = True
                st.error(error_msg)
                
            except Exception as e:
                error_msg = f"❌ Unexpected error: {type(e).__name__}: {str(e)}"
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.error(error_msg)
                
        st.rerun()

# ========================
#    SCHEDULED TASKS
# ========================
with tab2:
    st.header("📋 All Scheduled Tasks")
    cols = st.columns([1, 3])
    with cols[0]:
        refresh = st.button("🔄 Refresh Tasks")

    should_load = st.session_state.get("_reload_tasks_once", True) or refresh
    if should_load:
        with st.spinner("📥 Loading tasks..."):
            try:
                res = requests.post(
                    GET_ALL_TASKS_ENDPOINT,
                    timeout=REQUEST_TIMEOUT
                )
                
                if res.status_code == 200:
                    try:
                        data = res.json()
                        reports = data.get("reports", [])
                        tasks = reports[0] if reports and isinstance(reports[0], list) else []
                        
                        if tasks:
                            import pandas as pd
                            # Flatten each task to extract id and context fields
                            flat_tasks = []
                            for t in tasks:
                                try:
                                    context = t.get('context', {})
                                    flat_tasks.append({
                                        'id': t.get('id', 'N/A'),
                                        'task': context.get('task', 'N/A'),
                                        'date': context.get('date', 'N/A'),
                                        'time': context.get('time', 'N/A'),
                                        'status': context.get('status', 'pending')
                                    })
                                except Exception as e:
                                    st.warning(f"⚠️ Skipped malformed task: {str(e)}")
                                    continue
                            
                            if flat_tasks:
                                df = pd.DataFrame(flat_tasks)
                                st.dataframe(
                                    df[['task', 'date', 'time', 'status']], 
                                    use_container_width=True, 
                                    hide_index=True
                                )
                                st.success(f"✅ Loaded {len(flat_tasks)} task(s)")
                            else:
                                st.info("ℹ️ No valid tasks to display.")
                        else:
                            st.info("ℹ️ No scheduled tasks found. Add tasks via the chat!")
                        
                        st.session_state.backend_error = False
                        
                    except ValueError as e:
                        st.error(f"❌ Error parsing tasks data: Invalid JSON. {str(e)}")
                    except KeyError as e:
                        st.error(f"❌ Missing expected field in response: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Error processing tasks: {type(e).__name__}: {str(e)}")
                        
                elif res.status_code == 404:
                    st.error("❌ Tasks endpoint not found. Is the backend running correctly?")
                    st.session_state.backend_error = True
                    
                elif res.status_code == 500:
                    st.error("❌ Backend server error while fetching tasks. Check backend logs.")
                    
                else:
                    st.error(f"❌ Unexpected error: HTTP {res.status_code}")
                    
            except requests.exceptions.Timeout:
                st.error(f"⏱️ Request timed out after {REQUEST_TIMEOUT} seconds.")
                st.session_state.backend_error = True
                
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to backend at {BASE_URL}. Make sure it's running.")
                st.session_state.backend_error = True
                st.info("💡 Start the backend with: `jac serve backend/main.jac`")
                
            except Exception as e:
                st.error(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
                
        st.session_state._reload_tasks_once = False
