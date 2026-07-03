import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno
import io
import base64

# ==========================================
# SYSTEM CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="Enterprise Media & Serialization Suite",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Theme Injections via Custom Markdown
st.markdown("""
    <style>
        .reportview-container { background: #1A1C1E; }
        .sidebar .sidebar-content { background: #111214; }
        h1, h2, h3 { color: #FFFFFF; font-weight: 700; }
        .stButton>button { background-color: #00F5FF; color: #1A1C1E; font-weight: bold; border-radius: 6px; }
        .stButton>button:hover { background-color: #00D2DD; color: #1A1C1E; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# WORKSPACE NAVIGATION
# ==========================================
st.sidebar.title("🎛️ Architecture Control Center")
workspace_mode = st.sidebar.radio(
    "Select Target Functional Module:",
    ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"]
)

st.sidebar.markdown("---")

# ==========================================
# MODULE A: ADVANCED IMAGE STUDIO
# ==========================================
if workspace_mode == "🎨 Advanced Image Studio":
    st.title("🎨 Advanced Image Studio")
    st.caption("High-fidelity matrix manipulation canvas and optimization pipeline.")

    uploaded_file = st.file_uploader("Upload Target Asset Matrix", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        try:
            # Load asset into operational memory
            img_bytes = uploaded_file.read()
            original_image = Image.open(io.BytesIO(img_bytes))
            orig_w, orig_h = original_image.size
            
            # Metric Tracking for Optimization Phase
            input_bytesize = len(img_bytes) / 1024.0

            # --- Sidebar Controls ---
            st.sidebar.header("🔧 Processing Context")
            
            selected_filter = st.sidebar.selectbox(
                "Visual Filter Vector:",
                [
                    "Original", "Black & White", "Sepia Tone", "Gaussian Blur", 
                    "Contour Sketch", "Vibrant Saturation", "Retro Negative", "Emboss Art"
                ]
            )

            st.sidebar.markdown("### ✂️ Direct Canvas Manipulation")
            crop_top = st.sidebar.number_input("Crop Top (px)", min_value=0, max_value=orig_h-1, value=0)
            crop_bottom = st.sidebar.number_input("Crop Bottom (px)", min_value=0, max_value=orig_h, value=0)
            crop_left = st.sidebar.number_input("Crop Left (px)", min_value=0, max_value=orig_w-1, value=0)
            crop_right = st.sidebar.number_input("Crop Right (px)", min_value=0, max_value=orig_w, value=0)

            st.sidebar.markdown("### 📐 Scale Transformation")
            resize_option = st.sidebar.checkbox("Apply Dimensions Mutation", value=False)
            target_w = st.sidebar.slider("Target Width (px)", 16, orig_w * 2, orig_w)
            target_h = st.sidebar.slider("Target Height (px)", 16, orig_h * 2, orig_h)

            st.sidebar.markdown("### 🗜️ Serialization Optimization")
            compression_quality = st.sidebar.slider("Quantization Engine Quality (1-100)", 1, 100, 85)

            # --- Structural Mutation Pipeline Execution ---
            with st.spinner("Processing structural mutations..."):
                processed_image = original_image.copy()

                # Execution Shield: Direct Canvas Manipulation (Crop)
                try:
                    left_bound = crop_left
                    top_bound = crop_top
                    right_bound = orig_w - crop_right
                    bottom_bound = orig_h - crop_bottom
                    
                    if right_bound > left_bound and bottom_bound > top_bound:
                        processed_image = processed_image.crop((left_bound, top_bound, right_bound, bottom_bound))
                    elif crop_left > 0 or crop_top > 0 or crop_right > 0 or crop_bottom > 0:
                        st.warning("⚠️ Invalid Crop Topology boundaries detected. Reverting to structural fallback bounds.")
                except Exception as crop_err:
                    st.error(f"❌ Crop Execution Collision: {str(crop_err)}")

                # Execution Shield: Scale Transformation
                if resize_option:
                    try:
                        processed_image = processed_image.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    except Exception as resize_err:
                        st.error(f"❌ Scale Transformation Interrupted: {str(resize_err)}")

                # Execution Shield: Image Convolution Filter Array
                try:
                    if selected_filter == "Black & White":
                        processed_image = ImageOps.grayscale(processed_image)
                    elif selected_filter == "Sepia Tone":
                        gray = ImageOps.grayscale(processed_image)
                        processed_image = ImageOps.colorize(gray, "#704214", "#C0B283")
                    elif selected_filter == "Gaussian Blur":
                        processed_image = processed_image.filter(ImageFilter.GaussianBlur(radius=5))
                    elif selected_filter == "Contour Sketch":
                        processed_image = processed_image.filter(ImageFilter.CONTOUR)
                    elif selected_filter == "Vibrant Saturation":
                        enhancer = ImageEnhance.Color(processed_image)
                        processed_image = enhancer.enhance(2.0)
                    elif selected_filter == "Retro Negative":
                        if processed_image.mode != "RGB":
                            processed_image = processed_image.convert("RGB")
                        processed_image = ImageOps.invert(processed_image)
                    elif selected_filter == "Emboss Art":
                        processed_image = processed_image.filter(ImageFilter.EMBOSS)
                except Exception as filter_err:
                    st.error(f"❌ Convolution Layer Failure [{selected_filter}]: {str(filter_err)}")

            # --- Export Optimization Analysis ---
            try:
                out_buffer = io.BytesIO()
                # Determine format based on upload to avoid serialization conflicts
                out_format = "PNG" if original_image.format == "PNG" else "JPEG"
                processed_image.save(out_buffer, format=out_format, quality=compression_quality)
                output_bytes = out_buffer.getvalue()
                output_bytesize = len(output_bytes) / 1024.0
                delta = ((output_bytesize - input_bytesize) / input_bytesize) * 100
            except Exception as compression_err:
                st.error(f"❌ Optimization Engine Pipeline Failure: {str(compression_err)}")
                output_bytes = img_bytes
                output_bytesize = input_bytesize
                delta = 0.0

            # --- High-Fidelity UI Grid Rendering ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📸 Source Matrix Input")
                st.image(original_image, use_container_width=True)
                st.metric("Source Payload Volume", f"{input_bytesize:.2f} KB")

            with col2:
                st.markdown(f"### ✨ Rendered Output Canvas ({selected_filter})")
                st.image(processed_image, use_container_width=True)
                st.metric(
                    label="Optimized Payload Volume",
                    value=f"{output_bytesize:.2f} KB",
                    delta=f"{delta:.2f}% Weight Delta",
                    delta_color="inverse"
                )

            st.markdown("---")
            st.download_button(
                label="📥 Export Mutated Matrix Asset",
                data=output_bytes,
                file_name=f"processed_canvas.{out_format.lower()}",
                mime=f"image/{out_format.lower()}",
                use_container_width=True
            )

        except Exception as system_err:
            st.error(f"💥 Global Application Runtime Exception context triggered: {str(system_err)}")
    else:
        st.info("💡 Standby: System is awaiting binary upload stream to mount the image canvas pipelines.")

# ==========================================
# MODULE B: UNIVERSAL QR ENGINE
# ==========================================
elif workspace_mode == "🔮 Universal QR Engine":
    st.title("🔮 Universal QR Engine")
    st.caption("High-density multi-pipeline matrix encoding system with micro-styling overrides.")

    # Stylization Configuration Hooks
    st.sidebar.header("🎨 Matrix Stylization Overrides")
    dark_color = st.sidebar.color_picker("Matrix Module Color (Dark)", value="#1A1C1E")
    light_color = st.sidebar.color_picker("Canvas Background Color (Light)", value="#FFFFFF")
    matrix_scale = st.sidebar.slider("Module Scale Factor", 1, 20, 10)

    # Sub-Engine Context Multiplexer
    pipeline_mode = st.tabs(["🔤 Text to QR Pipeline", "🔗 Link to QR Pipeline", "🖼️ Image to QR Pipeline"])

    payload_data = None
    engine_ready = False

    # Pipeline 1: Text Literal Specification
    with pipeline_mode[0]:
        st.markdown("### Literal Character Encoding Pipeline")
        text_input = st.text_area("Input Literal Multi-Line Paragraph Text Payload", value="", placeholder="Enter target sequence content here...")
        if text_input.strip():
            payload_data = text_input
            engine_ready = True

    # Pipeline 2: Absolute Link Reference Specification
    with pipeline_mode[1]:
        st.markdown("### Absolute Uniform Resource Identifier Pipeline")
        url_input = st.text_input("Target Redirect Uniform Resource Identifier (URL)", value="", placeholder="https://www.example.com")
        if url_input.strip():
            # Minimal safety checks
            if not url_input.startswith(("http://", "https://")):
                st.warning("⚠️ Nonstandard Protocol Vector Detected. Ensure the target layout explicitly resolves on-device.")
            payload_data = url_input
            engine_ready = True

    # Pipeline 3: Binary Encoded Image Ingestion
    with pipeline_mode[2]:
        st.markdown("### Data Block Base64 Serialization Pipeline")
        qr_image_file = st.file_uploader("Upload Secondary Asset for Base64 Matrix Ingestion", type=["png", "jpg", "jpeg"], key="qr_img")
        
        if qr_image_file is not None:
            try:
                with st.spinner("Executing structural binary Base64 chunking sequence..."):
                    raw_binary_blocks = qr_image_file.read()
                    encoded_b64_string = base64.b64encode(raw_binary_blocks).decode("utf-8")
                    # Construct structurally compliant Data URI Scheme representation
                    mime_type = qr_image_file.type
                    payload_data = f"data:{mime_type};base64,{encoded_b64_string}"
                    
                    st.success(f"⚡ Binary payload successfully serialized into dynamic base64 data-block string structure ({len(payload_data)} characters).")
                    engine_ready = True
            except Exception as b64_err:
                st.error(f"❌ Base64 Serialization Sequence Halted: {str(b64_err)}")

    # Matrix Compilation Engine and Presentation Boundary
    if engine_ready and payload_data:
        st.markdown("---")
        st.markdown("### 🎚️ Compiled Matrix Output Canvas")
        
        try:
            with st.spinner("Compiling QR Module Geometric Arrays..."):
                # Construct high-density data matrix sequence via micro-shielding containment
                qr_matrix = segno.make_qr(payload_data, error='M')
                
                # Render to memory array block buffer
                qr_buffer = io.BytesIO()
                qr_matrix.save(
                    qr_buffer, 
                    kind='png', 
                    dark=dark_color, 
                    light=light_color, 
                    scale=matrix_scale
                )
                qr_output_bytes = qr_buffer.getvalue()

            # Dynamic Grid Interface Display
            col_ui_left, col_ui_right = st.columns([1, 2])
            with col_ui_left:
                st.image(qr_output_bytes, caption="Active Matrix Manifestation", use_container_width=False)
            
            with col_ui_right:
                st.markdown("#### Matrix Metadata Profile")
                st.info(f"🧬 **Matrix Design Version:** {qr_matrix.version}\n\n"
                        f"🛡️ **Error Correction Metric:** Level M (Medium Quality Protection)\n\n"
                        f"📦 **Total Encoded String Length:** {len(payload_data)} characters")
                
                st.download_button(
                    label="📥 Download Compiled QR Matrix Asset",
                    data=qr_output_bytes,
                    file_name="compiled_matrix_output.png",
                    mime="image/png",
                    use_container_width=True
                )
        except Exception as matrix_err:
            st.error(f"❌ Matrix Generation Failure: The input payload bounds may exceed the maximum capacity configurations of the target matrix standard. Breakdown Context: {str(matrix_err)}")
    else:
        st.info("💡 Standby: Core structural engines are idling until valid payload parameters are registered within an active pipeline.")
