import streamlit as st
import subprocess
import tempfile
import os

st.set_page_config(
    page_title="MP4 → WebM Converter",
    page_icon="🎬",
    layout="centered"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0d0d0d;
    color: #f0f0f0;
}

.stApp {
    background: #0d0d0d;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
}

.hero h1 {
    font-size: 3rem;
    background: linear-gradient(135deg, #ff6b35, #f7c59f, #ff6b35);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    margin-bottom: 0.25rem;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.hero p {
    color: #888;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
}

.card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
}

.settings-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

.tag {
    display: inline-block;
    background: #ff6b3520;
    color: #ff6b35;
    border: 1px solid #ff6b3540;
    border-radius: 6px;
    padding: 2px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    margin: 2px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #ff6b35, #e85d25);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: opacity 0.2s;
}

.stButton > button:hover {
    opacity: 0.85;
}

.stFileUploader {
    background: #1a1a1a;
    border-radius: 12px;
}

.stSlider > div { color: #f0f0f0; }

.success-box {
    background: #0f2a1a;
    border: 1px solid #1a5c35;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #4ade80;
}

.error-box {
    background: #2a0f0f;
    border: 1px solid #5c1a1a;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #f87171;
}

.info-row {
    display: flex;
    justify-content: space-between;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #666;
    border-top: 1px solid #2a2a2a;
    padding-top: 1rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 MP4 → WebM</h1>
    <p>SCREEN RECORDING CONVERTER · POWERED BY FFMPEG</p>
</div>
""", unsafe_allow_html=True)


# ── Upload ───────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="settings-label">📁 Upload your MP4 file</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["mp4"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)


# ── Settings ─────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="settings-label">⚙️ Conversion Settings</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    crf = st.slider(
        "Quality (CRF)",
        min_value=15, max_value=50, value=30,
        help="Lower = better quality, larger file. 28–35 is ideal for screen recordings."
    )

with col2:
    audio_bitrate = st.selectbox(
        "Audio Bitrate",
        options=["64k", "96k", "128k", "192k"],
        index=2
    )

st.markdown(f"""
<div class="info-row">
    <span>Video codec: <span style="color:#ff6b35">libvpx-vp9</span></span>
    <span>Audio codec: <span style="color:#ff6b35">libopus</span></span>
    <span>CRF: <span style="color:#ff6b35">{crf}</span></span>
    <span>Audio: <span style="color:#ff6b35">{audio_bitrate}</span></span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Convert ──────────────────────────────────────────────────────────────────
if uploaded_file:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#888; margin-bottom:1rem;">
        📄 <b style="color:#f0f0f0">{uploaded_file.name}</b> &nbsp;·&nbsp; {file_size_mb:.2f} MB
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Convert to WebM"):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save uploaded MP4
            input_path = os.path.join(tmpdir, uploaded_file.name)
            output_name = os.path.splitext(uploaded_file.name)[0] + ".webm"
            output_path = os.path.join(tmpdir, output_name)

            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            # Run FFmpeg
            with st.spinner("⏳ Converting... this may take a moment."):
                command = [
                    "ffmpeg", "-y",
                    "-loglevel", "quiet",
                    "-i", input_path,
                    "-c:v", "libvpx-vp9",
                    "-crf", str(crf),
                    "-b:v", "0",
                    "-cpu-used", "4",
                    "-deadline", "realtime",
                    "-c:a", "libopus",
                    "-b:a", audio_bitrate,
                    output_path
                ]
                result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0 and os.path.exists(output_path):
                output_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                saved = ((file_size_mb - output_size_mb) / file_size_mb) * 100

                st.markdown(f"""
                <div class="success-box">
                    ✅ Conversion successful!<br>
                    📦 Output: <b>{output_name}</b><br>
                    📉 Size: {file_size_mb:.2f} MB → {output_size_mb:.2f} MB
                    ({saved:.1f}% smaller)
                </div>
                """, unsafe_allow_html=True)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download WebM",
                        data=f,
                        file_name=output_name,
                        mime="video/webm"
                    )
            else:
                st.markdown(f"""
                <div class="error-box">
                    ❌ Conversion failed.<br>
                    Make sure FFmpeg is installed on your system.<br><br>
                    <b>Error:</b> {result.stderr[-500:] if result.stderr else 'Unknown error'}
                </div>
                """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; color:#444; font-family:'Space Mono',monospace;
                font-size:0.8rem; padding: 1rem 0;">
        ↑ Upload an MP4 file to get started
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#333; font-family:'Space Mono',monospace;
            font-size:0.7rem; margin-top:3rem; padding-bottom:1rem;">
    Requires FFmpeg installed · VP9 + Opus · WebM Format
</div>
""", unsafe_allow_html=True)