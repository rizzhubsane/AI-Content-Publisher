import streamlit as st
from reformatter import generate_reformatted_content
from poster import post_to_devto, post_to_hashnode
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Content Publisher",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with modern design and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styles */
    .main-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        animation: slideInFromTop 0.8s ease-out;
    }
    
    .main-header h1 {
        color: #f8fafc;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .main-header p {
        color: #cbd5e1;
        font-size: 1.25rem;
        font-weight: 400;
        margin: 0;
        opacity: 0.9;
    }
    
    /* Section Headers */
    .section-header {
        color: #f1f5f9;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding: 1rem 0;
        border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    /* Status Cards */
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        animation: slideInFromRight 0.6s ease-out;
    }
    
    .success-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        border-color: rgba(16, 185, 129, 0.3);
        color: #86efac;
    }
    
    .error-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        border-color: rgba(239, 68, 68, 0.3);
        color: #fca5a5;
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
        border-color: rgba(245, 158, 11, 0.3);
        color: #fde68a;
    }
    
    .info-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
        border-color: rgba(59, 130, 246, 0.3);
        color: #93c5fd;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 16px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.5);
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .stCheckbox > label:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(59, 130, 246, 0.3);
        transform: translateY(-1px);
    }
    
    .stCheckbox > label > span {
        color: #f1f5f9;
        font-weight: 500;
    }
    
    /* Text Area */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: scaleIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 10px;
        height: 12px;
        animation: progressGlow 2s ease-in-out infinite alternate;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #f1f5f9;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 0 0 12px 12px;
        color: #e2e8f0;
    }
    
    /* Text Styles */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f8fafc;
        font-weight: 600;
    }
    
    .stMarkdown p {
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    .stCaption {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* Animations */
    @keyframes slideInFromTop {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInFromRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes progressGlow {
        from {
            box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
        }
        to {
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.8);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
    }
</style>
""", unsafe_allow_html=True)

# Header section with animation
st.markdown("""
<div class="main-header">
    <h1>✨✨ AI Content Publisher✨✨</h1>
    <p>Transform your content for multiple platforms with AI-powered optimization</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'publishing_status' not in st.session_state:
    st.session_state.publishing_status = {}
if 'published_urls' not in st.session_state:
    st.session_state.published_urls = {}

# Main layout with columns
col1, col2 = st.columns([2.5, 1.5], gap="large")

with col1:
    # Input Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📝 Content Input</div>', unsafe_allow_html=True)
    
    master_article = st.text_area(
        "Paste your master article here",
        height=300,
        placeholder="Enter your article content here...",
        help="This will be the source content that gets reformatted for each platform",
        label_visibility="collapsed"
    )
    
    # Word count with animation
    if master_article:
        word_count = len(master_article.split())
        st.markdown(f'<div style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem; animation: fadeInUp 0.3s ease-out;">📊 Word count: <span style="color: #3b82f6; font-weight: 600;">{word_count}</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Platform Selection
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🎯 Platform Selection</div>', unsafe_allow_html=True)
    
    platform_col1, platform_col2 = st.columns(2)
    
    with platform_col1:
        devto_selected = st.checkbox("📱 Dev.to", help="Publish to Dev.to community")
    
    with platform_col2:
        hashnode_selected = st.checkbox("🔗 Hashnode", help="Publish to Hashnode blog")
    
    platforms = []
    if devto_selected:
        platforms.append("Dev.to")
    if hashnode_selected:
        platforms.append("Hashnode")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Publishing Button
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🚀 Publishing Control</div>', unsafe_allow_html=True)
    
    # Center the button
    button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
    
    with button_col2:
        publish_button = st.button("🚀 Publish to Selected Platforms", type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Status sidebar
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Publishing Status</div>', unsafe_allow_html=True)
    
    if platforms:
        for platform in platforms:
            status = st.session_state.publishing_status.get(platform, "pending")
            
            if status == "pending":
                st.markdown(f'<div class="status-card info-card">⏳ <strong>{platform}</strong>: Ready to publish</div>', unsafe_allow_html=True)
            elif status == "processing":
                st.markdown(f'<div class="status-card warning-card pulse">⚡ <strong>{platform}</strong>: Processing...</div>', unsafe_allow_html=True)
            elif status == "success":
                st.markdown(f'<div class="status-card success-card">✅ <strong>{platform}</strong>: Published</div>', unsafe_allow_html=True)
            elif status == "error":
                st.markdown(f'<div class="status-card error-card">❌ <strong>{platform}</strong>: Failed</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-card info-card">Select platforms to see status</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Publishing Logic
if publish_button:
    if not master_article.strip():
        st.markdown('<div class="glass-card error-card">⚠️ Please paste a master article before publishing.</div>', unsafe_allow_html=True)
    elif not platforms:
        st.markdown('<div class="glass-card error-card">⚠️ Please select at least one platform.</div>', unsafe_allow_html=True)
    else:
        # Clear previous status
        st.session_state.publishing_status = {}
        st.session_state.published_urls = {}
        
        # Create progress container
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📈 Publishing Progress</div>', unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_platforms = len(platforms)
        
        for i, platform in enumerate(platforms):
            # Update progress
            progress_percentage = i / total_platforms
            progress_bar.progress(progress_percentage)
            status_text.markdown(f'<div style="color: #cbd5e1; font-weight: 500; text-align: center; margin: 1rem 0;">Processing {platform}...</div>', unsafe_allow_html=True)
            
            # Update session state
            st.session_state.publishing_status[platform] = "processing"
            st.rerun()
            
            try:
                # Generate reformatted content
                result = generate_reformatted_content(platform, master_article)
                title = result["title"]
                content = result["content"]
                tags = result["tags"]
                
                # Post to platform
                if platform == "Dev.to":
                    url = post_to_devto(title, content, tags=tags, publish=True)
                elif platform == "Hashnode":
                    url = post_to_hashnode(title, content, tags=tags, publish=True)
                
                # Update success status
                st.session_state.publishing_status[platform] = "success"
                st.session_state.published_urls[platform] = {
                    "url": url,
                    "title": title,
                    "tags": tags
                }
                
            except Exception as e:
                st.session_state.publishing_status[platform] = "error"
                st.session_state.published_urls[platform] = {
                    "error": str(e)
                }
        
        # Complete progress
        progress_bar.progress(1.0)
        status_text.markdown('<div style="color: #86efac; font-weight: 600; text-align: center; margin: 1rem 0;">✅ Publishing complete!</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Small delay for better UX
        time.sleep(0.5)
        st.rerun()

# Results Section
if st.session_state.published_urls:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📋 Publishing Results</div>', unsafe_allow_html=True)
    
    success_count = 0
    error_count = 0
    
    for platform, data in st.session_state.published_urls.items():
        if "error" in data:
            error_count += 1
            with st.expander(f"❌ {platform} - Failed", expanded=False):
                st.markdown(f'<div class="error-card">**Error:** {data["error"]}</div>', unsafe_allow_html=True)
        else:
            success_count += 1
            with st.expander(f"✅ {platform} - Published Successfully", expanded=True):
                st.markdown(f'<div class="success-card"><strong>🎉 Successfully published to {platform}!</strong></div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**📝 Title:** {data['title']}")
                    st.markdown(f"**🏷️ Tags:** `{', '.join(data['tags'])}`")
                
                with col2:
                    st.markdown(f"**🔗 Live URL:**")
                    st.markdown(f"[**View Published Post →**]({data['url']})")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary metrics
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Summary</div>', unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Platforms", len(st.session_state.published_urls))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Successful", success_count, delta=success_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Failed", error_count, delta=error_count if error_count > 0 else None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 3rem 0; margin-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
    <p style="font-size: 1rem; margin: 0;">Made by Rishabh Sain using Streamlit • Powered by AI</p>
    <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0; opacity: 0.7;">© 2024 AI Content Publisher</p>
</div>
""", unsafe_allow_html=True)