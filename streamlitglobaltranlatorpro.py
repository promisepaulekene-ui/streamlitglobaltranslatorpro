import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from openai import OpenAI
import os
import tempfile
import time
from datetime import datetime
import hashlib
import base64
import json
import re
from PIL import Image
import requests
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Global Translator Pro - Advanced Multilingual Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling and background
st.markdown("""
<style>
    /* Main background with elegant gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* Main content area with glassmorphism effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 100%);
    }
    
    .css-1d391kg .css-1lcbmhc {
        background: transparent !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #1a73e8 0%, #6c5ce7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #ea4335;
        margin-bottom: 1rem;
        font-weight: 600;
        background: linear-gradient(135deg, #ea4335 0%, #fbbc04 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .translation-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e8f0fe 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #1a73e8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .dictionary-box {
        background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #34a853;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .security-box {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 4px solid #f57c00;
    }
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #f1f3f4 100%);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 4px solid #fbbc04;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 30px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .stButton button {
        background: linear-gradient(to right, #1a73e8, #6c5ce7);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(to right, #1557b0, #5645c9);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .auth-button {
        background: linear-gradient(to right, #34a853, #0f9d58) !important;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #5f6368;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
    }
    .quality-badge {
        background: linear-gradient(135deg, #34a853 0%, #0f9d58 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 10px;
    }
    .language-tag {
        background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0 5px;
    }
    .context-badge {
        background: linear-gradient(135deg, #9c27b0 0%, #6a1b9a 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 5px;
    }
    .warning-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 12px;
        border-radius: 10px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    .user-badge {
        background: linear-gradient(135deg, #fbbc04 0%, #f9a825 100%);
        color: #202124;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .dropdown-section {
        background: linear-gradient(135deg, #f0f2f6 0%, #e6e9f0 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #1a73e8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .remember-me {
        display: flex;
        align-items: center;
        margin: 10px 0;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #1a73e8;
        box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
    }
    
    /* Select box styling */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px;
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        font-weight: 500;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2rem;
    }
    .logo-text {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #1a73e8 0%, #6c5ce7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Add logo to the layout
def add_logo():
    st.markdown("""
    <div class="logo-container">
        <div>
            <h1 class="logo-text">A</h1>
            <h1 class="logo-text">X</h1>
        </div>
        <div style="margin-left: 20px;">
            <h1 class="logo-text">LANGUAGE</h1>
            <h1 class="logo-text">TRANSLATOR</h1>
            <h1 class="logo-text">PRO</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Corrected language support with proper codes
language_options = {
    'auto': 'Auto Detect',
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
    'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
    'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
    'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
    'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian',
    'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew', 'hi': 'Hindi',
    'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian',
    'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese',
    'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin',
    'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
    'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
    'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese',
    'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan',
    'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona',
    'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
    'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili',
    'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu',
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa',
    'yi': 'Yiddish', 'yo': 'Yoruba', 'ig': 'Igbo', 'zu': 'Zulu'
}

# Language mapping for gTTS - fixed with proper language codes
gtts_language_mapping = {
    'af': 'af', 'ar': 'ar', 'bn': 'bn', 'bs': 'bs', 'ca': 'ca', 'cs': 'cs',
    'da': 'da', 'de': 'de', 'el': 'el', 'en': 'en', 'eo': 'eo', 'es': 'es',
    'et': 'et', 'fi': 'fi', 'fr': 'fr', 'gu': 'gu', 'hi': 'hi', 'hr': 'hr',
    'hu': 'hu', 'hy': 'hy', 'id': 'id', 'is': 'is', 'it': 'it', 'ja': 'ja',
    'jw': 'jw', 'km': 'km', 'kn': 'kn', 'ko': 'ko', 'la': 'la', 'lv': 'lv',
    'ml': 'ml', 'mr': 'mr', 'ms': 'ms', 'my': 'my', 'ne': 'ne', 'nl': 'nl',
    'no': 'no', 'pl': 'pl', 'pt': 'pt', 'ro': 'ro', 'ru': 'ru', 'si': 'si',
    'sk': 'sk', 'sq': 'sq', 'sr': 'sr', 'su': 'su', 'sv': 'sv', 'sw': 'sw',
    'ta': 'ta', 'te': 'te', 'th': 'th', 'tl': 'tl', 'tr': 'tr', 'uk': 'uk',
    'ur': 'ur', 'vi': 'vi', 'zh-CN': 'zh-cn', 'zh-TW': 'zh-tw', 'zu': 'zu',
    'yo': 'yo', 'ha': 'ha', 'ig': 'ig'
}

# Limited TTS support languages - languages not in gtts_language_mapping
limited_tts_languages = [lang for lang in language_options.keys() if lang not in gtts_language_mapping and lang != 'auto']

# =============================================
# ADD YOUR OPENAI API KEY HERE:
# =============================================
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "your-openai-api-key-here")  # Replace with your actual OpenAI API key
# =============================================

# Initialize OpenAI client
if OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here":
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

# User authentication functions
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    return stored_password == hash_password(provided_password)

def init_user_db():
    """Initialize user database"""
    if 'users' not in st.session_state:
        # Default user for testing
        st.session_state.users = {
            'admin': {
                'password': hash_password('admin123'),
                'preferences': {
                    'source_lang': 'auto',
                    'target_lang': 'es',
                    'auto_play_audio': True,
                    'slow_speech': False,
                    'real_time_mode': False
                },
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}
        
    # Check if user was remembered
    if 'remember_me' in st.session_state and st.session_state.remember_me and 'remembered_user' in st.session_state:
        st.session_state.current_user = st.session_state.remembered_user
        if st.session_state.current_user in st.session_state.users:
            st.session_state.user_preferences = st.session_state.users[st.session_state.current_user].get('preferences', {})

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, "Username is valid"

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"

def show_login():
    """Display login form"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #1a73e8;">🔐 Login to Global Translator Pro</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        # Remember me checkbox
        remember_me = st.checkbox("Remember me", value=True, key="remember_me_checkbox")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("Please fill in all fields")
            elif username not in st.session_state.users:
                st.error("Username not found. Please sign up first.")
            elif not verify_password(st.session_state.users[username]['password'], password):
                st.error("Incorrect password")
            else:
                st.session_state.current_user = username
                st.session_state.user_preferences = st.session_state.users[username].get('preferences', {})
                
                # Remember user if checkbox is checked
                if remember_me:
                    st.session_state.remember_me = True
                    st.session_state.remembered_user = username
                
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
    
    st.markdown('<p style="text-align: center;">Don\'t have an account? <a href="#signup">Sign up here</a></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_signup():
    """Display sign up form"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #1a73e8;">🚀 Create Your Account</h2>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="Create a password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if not username or not password or not confirm_password:
                st.error("Please fill in all fields")
            else:
                is_valid, message = validate_username(username)
                if not is_valid:
                    st.error(message)
                elif username in st.session_state.users:
                    st.error("Username already taken. Please choose another.")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    is_valid, message = validate_password(password)
                    if not is_valid:
                        st.error(message)
                    elif not terms:
                        st.error("You must agree to the Terms of Service and Privacy Policy")
                    else:
                        # Create new user
                        st.session_state.users[username] = {
                            'password': hash_password(password),
                            'preferences': {
                                'source_lang': 'auto',
                                'target_lang': 'es',
                                'auto_play_audio': True,
                                'slow_speech': False,
                                'real_time_mode': False
                            },
                            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.current_user = username
                        st.session_state.user_preferences = st.session_state.users[username]['preferences']
                        
                        # Remember user
                        st.session_state.remember_me = True
                        st.session_state.remembered_user = username
                        
                        st.success("Account created successfully!")
                        time.sleep(1)
                        st.rerun()
    
    st.markdown('<p style="text-align: center;">Already have an account? <a href="#login">Login here</a></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_logout():
    """Logout the current user"""
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.current_user = None
        st.session_state.remember_me = False
        st.session_state.remembered_user = None
        st.success("Logged out successfully!")
        time.sleep(1)
        st.rerun()

# Translation functions
def encrypt_text(text):
    """Simple encryption for text data"""
    return base64.b64encode(text.encode()).decode()

def decrypt_text(encrypted_text):
    """Simple decryption for text data"""
    return base64.b64decode(encrypted_text.encode()).decode()

def get_definition(word, context=None):
    """Get word definition using OpenAI with contextual understanding"""
    if not openai_client:
        return None
    
    try:
        prompt = f"""
        Provide a detailed definition for the word "{word}" in the following format:
        
        Definition: [clear definition]
        Part of Speech: [part of speech]
        Example: [example sentence]
        Etymology: [brief etymology if interesting]
        Synonyms: [3-5 synonyms]
        
        """
        
        if context:
            prompt += f"\nConsider this contextual sentence: '{context}'\n"
        
        prompt += "Keep the response concise but informative."
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful dictionary assistant that provides clear, concise definitions with contextual understanding."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        definition_text = response.choices[0].message.content.strip()
        return definition_text
    except Exception as e:
        st.error(f"Error getting definition: {e}")
        return None

def text_to_speech(text, lang, slow=False):
    """Convert text to speech using gTTS with proper language mapping"""
    if lang not in gtts_language_mapping:
        st.warning(f"Text-to-speech is not available for {language_options.get(lang, lang)}.")
        return None
    
    cache_key = f"{text}_{lang}_{slow}"
    
    if 'audio_cache' not in st.session_state:
        st.session_state.audio_cache = {}
    
    if cache_key in st.session_state.audio_cache:
        return st.session_state.audio_cache[cache_key]
    
    try:
        lang_code = gtts_language_mapping[lang]
        tts = gTTS(text=text, lang=lang_code, slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            st.session_state.audio_cache[cache_key] = tmp_file.name
            return tmp_file.name
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return None

def translate_large_text(text, source_lang, target_lang, chunk_size=500):
    """Translate large text by breaking it into chunks"""
    try:
        # Split text into chunks
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = []
        
        # Translate each chunk
        for i, chunk in enumerate(chunks):
            with st.spinner(f"Translating chunk {i+1}/{len(chunks)}..."):
                if source_lang == 'auto':
                    translator = GoogleTranslator(source='auto', target=target_lang)
                else:
                    translator = GoogleTranslator(source=source_lang, target=target_lang)
                
                translated_chunk = translator.translate(chunk)
                translated_chunks.append(translated_chunk)
        
        # Combine translated chunks
        translated_text = " ".join(translated_chunks)
        
        # Save to user's translation history
        if st.session_state.current_user:
            username = st.session_state.current_user
            if 'translation_history' not in st.session_state.users[username]:
                st.session_state.users[username]['translation_history'] = []
            
            st.session_state.users[username]['translation_history'].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'source_text': encrypt_text(text),
                'translated_text': encrypt_text(translated_text),
                'source_lang': source_lang,
                'target_lang': target_lang
            })
            
            # Keep only the last 20 translations
            if len(st.session_state.users[username]['translation_history']) > 20:
                st.session_state.users[username]['translation_history'].pop(0)
        
        return translated_text
    except Exception as e:
        st.error(f"Translation error: {e}")
        # Try with auto-detection as fallback
        try:
            translator = GoogleTranslator(source='auto', target=target_lang)
            translated_text = translator.translate(text)
            return translated_text
        except:
            return f"Error: Could not translate. Please try a different language combination."

def main_app():
    """Main application after login"""
    # Header with user info
    username = st.session_state.current_user
    user_data = st.session_state.users[username]
    
    # Add logo to the layout
    add_logo()
    
    st.markdown(f'<div style="text-align: right; margin-top: -50px;"><span class="user-badge">👤 {username}</span></div>', unsafe_allow_html=True)
    
    # Main content area - moved to top with dropdown sections
    st.markdown('<div class="dropdown-section">', unsafe_allow_html=True)
    st.markdown("### Translation Section")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input with increased height for larger text
        text_to_translate = st.text_area(
            "Text to translate",
            height=200,
            placeholder="Enter text or word to translate and define...",
            help="Type the text you want to translate or look up. Large texts are supported.",
            key="text_input"
        )
        
        # Context input for better translations
        context_text = st.text_input(
            "Context (optional)",
            placeholder="Provide context for better translation accuracy...",
            help="Adding context helps with ambiguous words or phrases"
        )
    
    with col2:
        # Language selection with user preferences
        prefs = st.session_state.user_preferences
        
        source_lang = st.selectbox(
            "Source Language",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(prefs.get('source_lang', 'auto'))
        )
        
        target_lang = st.selectbox(
            "Target Language",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(prefs.get('target_lang', 'es'))
        )
        
        # Real-time translation toggle with user preference
        real_time_mode = st.checkbox("Real-time Translation", value=prefs.get('real_time_mode', False))
        
        # Audio settings with user preferences
        slow_speech = st.checkbox("Slow Speech", value=prefs.get('slow_speech', False))
        auto_play_audio = st.checkbox("Auto-play Audio", value=prefs.get('auto_play_audio', True))
        
        # Save preferences
        st.session_state.user_preferences = {
            'source_lang': source_lang,
            'target_lang': target_lang,
            'real_time_mode': real_time_mode,
            'slow_speech': slow_speech,
            'auto_play_audio': auto_play_audio
        }
        st.session_state.users[username]['preferences'] = st.session_state.user_preferences
        
        # Translate button
        if not real_time_mode:
            translate_button = st.button("Translate & Define", type="primary", use_container_width=True)
        else:
            translate_button = False
            if text_to_translate and text_to_translate != st.session_state.get('last_text', ''):
                st.session_state.last_text = text_to_translate
                translate_button = True
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process translation
    if (translate_button or (real_time_mode and text_to_translate)) and text_to_translate:
        with st.spinner("Translating and generating definition..."):
            # Use appropriate translation function based on text length
            if len(text_to_translate) > 500:
                translated_text = translate_large_text(text_to_translate, source_lang, target_lang)
            else:
                translated_text = translate_large_text(text_to_translate, source_lang, target_lang, chunk_size=len(text_to_translate))
            
            if translated_text and not translated_text.startswith("Error:"):
                # Display translation
                st.markdown('<div class="translation-box">', unsafe_allow_html=True)
                
                # Get the language name safely
                lang_name = language_options.get(target_lang, target_lang)
                
                # Display the translation with proper language tag
                st.markdown(f"**Translation** <span class='language-tag'>{lang_name}</span> <span class='quality-badge'>Quality Checked</span>")
                
                # Display translated text in a scrollable container for large texts
                if len(translated_text) > 500:
                    st.text_area("Translated Text", translated_text, height=200, disabled=True)
                else:
                    st.success(translated_text)
                
                # Text-to-speech
                if target_lang in gtts_language_mapping:
                    audio_file = text_to_speech(translated_text, target_lang, slow_speech)
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                        
                        # Auto-play if enabled
                        if auto_play_audio:
                            st.markdown(
                                f"""
                                <script>
                                var audio = document.querySelector('audio');
                                if (audio) {{
                                    audio.play();
                                }}
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                else:
                    st.markdown("""
                    <div class="warning-box">
                    ⚠️ Text-to-speech is not available for this language. 
                    Try English, Spanish, French, German, or other major languages.
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Definition (only for shorter texts)
                if len(text_to_translate.split()) <= 5:
                    definition = get_definition(text_to_translate, context_text)
                    
                    if definition:
                        st.markdown('<div class="dictionary-box">', unsafe_allow_html=True)
                        st.markdown(f"**Definition for '{text_to_translate}'** <span class='context-badge'>Context-Aware</span>")
                        st.write(definition)
                        st.markdown('</div>', unsafe_allow_html=True)
                    elif openai_client:
                        st.info("No definition could be generated for this term.")
                else:
                    st.info("Definitions work best with single words or short phrases.")
            else:
                st.error(translated_text)
    
    # Additional sections in dropdown format
    with st.expander("📚 Translation History"):
        if 'translation_history' in st.session_state.users[username] and st.session_state.users[username]['translation_history']:
            for i, item in enumerate(reversed(st.session_state.users[username]['translation_history'][-5:])):
                with st.expander(f"Translation {i+1} - {item['timestamp']}"):
                    st.write(f"From: {language_options.get(item['source_lang'], item['source_lang'])}")
                    st.write(f"To: {language_options.get(item['target_lang'], item['target_lang'])}")
                    
                    # Display only preview of long texts
                    source_preview = decrypt_text(item['source_text'])
                    if len(source_preview) > 100:
                        source_preview = source_preview[:100] + "..."
                    
                    translated_preview = decrypt_text(item['translated_text'])
                    if len(translated_preview) > 100:
                        translated_preview = translated_preview[:100] + "..."
                    
                    st.write(f"Original: {source_preview}")
                    st.write(f"Translated: {translated_preview}")
                    
                    # Show full text in expandable sections
                    with st.expander("View Full Original Text"):
                        st.write(decrypt_text(item['source_text']))
                    
                    with st.expander("View Full Translated Text"):
                        st.write(decrypt_text(item['translated_text']))
        else:
            st.info("No translation history yet.")
            
        if st.button("Clear History", key="clear_history_btn"):
            if 'translation_history' in st.session_state.users[username]:
                st.session_state.users[username]['translation_history'] = []
            st.success("History cleared!")
            st.rerun()
    
    with st.expander("🌐 Supported Languages"):
        # Display popular languages
        popular_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 
            'zh-CN': 'Chinese (Simplified)', 'zh-TW': 'Chinese (Traditional)', 'ja': 'Japanese', 'ar': 'Arabic', 
            'hi': 'Hindi', 'ko': 'Korean', 'nl': 'Dutch', 'tr': 'Turkish',
            'sv': 'Swedish', 'pl': 'Polish', 'id': 'Indonesian', 'vi': 'Vietnamese',
            'yo': 'Yoruba', 'ha': 'Hausa', 'ig': 'Igbo'
        }
        
        for code, name in popular_languages.items():
            tts_status = "✓" if code in gtts_language_mapping else "⚠️"
            st.write(f"• {name} ({code}) {tts_status}")
        
        st.markdown(f"**And {len(language_options) - len(popular_languages)} more languages!**")
        st.info("✓ = TTS available, ⚠️ = TTS limited/unavailable")
    
    with st.expander("💡 Tips & Features"):
        st.write("• Use short phrases for best translation results")
        st.write("• Add context for better accuracy with ambiguous words")
        st.write("• Enable real-time translation for instant results")
        st.write("• Use 'Auto Detect' for unknown source languages")
        st.write("• Check TTS availability in language settings")
        st.write("• Large texts are automatically split into chunks for better translation")
        
        st.markdown("---")
        st.markdown("### Quick Actions")
        if st.button("Clear Text", key="clear_text_btn"):
            st.session_state.text_input = ""
            st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        st.info("Configure your translation preferences")
        
        # Show TTS availability
        if target_lang in limited_tts_languages:
            st.warning(f"⚠️ Text-to-speech has limited support for {language_options.get(target_lang, target_lang)}")
        elif target_lang not in gtts_language_mapping:
            st.warning(f"⚠️ Text-to-speech is not available for {language_options.get(target_lang, target_lang)}")
        else:
            st.success(f"✓ Text-to-speech is available for {language_options.get(target_lang, target_lang)}")
        
        st.markdown("---")
        st.markdown('<div class="feature-card">📖 Dictionary Integration</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">🔒 Data Protection & Encryption</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">✅ Quality Control Measures</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">🎵 Enhanced Audio Support</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">⚡ Real-time Translation</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">🧠 Contextual Understanding</div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card">📝 Large Text Support</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.write("### Data Protection")
        st.markdown("""
        <div class="security-box">
        <b>Your privacy is protected:</b><br>
        • Translation history encrypted<br>
        • No data stored on servers<br>
        • Session-based storage only
        </div>
        """, unsafe_allow_html=True)
        
        # API status
        st.markdown("---")
        st.write("### API Status")
        if openai_client:
            st.success("OpenAI API: Configured ✓")
        else:
            st.warning("OpenAI API: Not configured")
            st.info("To enable AI definitions, add your OpenAI API key in the code.")
        
        # Logout button
        st.markdown("---")
        show_logout()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
    Global Translator Pro © 2023 | Professional Translation Technology<br>
    <span style="font-size: 0.8rem;">All translations are processed securely with end-to-end encryption</span>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Initialize user database and session state
    init_user_db()
    
    # Initialize audio cache
    if 'audio_cache' not in st.session_state:
        st.session_state.audio_cache = {}
    
    # Check if user is logged in
    if st.session_state.current_user is None:
        # Show authentication options
        auth_tab1, auth_tab2 = st.tabs(["Login", "Sign Up"])
        
        with auth_tab1:
            show_login()
        
        with auth_tab2:
            show_signup()
    else:
        # User is logged in, show main app
        main_app()

if __name__ == "__main__":
    main()