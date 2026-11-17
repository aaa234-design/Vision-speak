import io
from collections import Counter

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from detector import OBJECTS, detect
from voice import speak

st.set_page_config(page_title="VisionSpeak", page_icon="👁️", layout="wide")

st.markdown("""
<style>
.main {background: linear-gradient(135deg, #101827 0%, #17243a 100%);}
.block-container {padding-top: 2rem; max-width: 1200px;}
.hero {padding: 1.5rem 1.8rem; border-radius: 18px; background: linear-gradient(120deg,#263b60,#3b2f66); color: white; margin-bottom: 1.2rem;}
.hero h1 {font-size: 2.5rem; margin: 0;}
.hero p {color: #d9e4ff; margin-bottom: 0;}
div[data-testid="stMetric"] {background: #1d2b40; padding: 14px; border-radius: 12px;}
</style>
<div class="hero">
<h1>👁️ VisionSpeak</h1>
<p>Smart object detection with automatic voice assistance · 100 everyday object categories</p>
</div>
""", unsafe_allow_html=True)

# Urdu names are spoken by a compatible Urdu Windows TTS voice.
URDU_NAMES = {
    "person": "شخص", "car": "گاڑی", "bus": "بس", "truck": "ٹرک",
    "motorcycle": "موٹر سائیکل", "bicycle": "سائیکل", "scooter": "اسکوٹر",
    "train": "ٹرین", "airplane": "ہوائی جہاز", "boat": "کشتی",
    "traffic light": "ٹریفک لائٹ", "stop sign": "رکنے کا نشان",
    "parking meter": "پارکنگ میٹر", "bench": "بینچ", "chair": "کرسی",
    "sofa": "صوفہ", "table": "میز", "desk": "ڈیسک", "bed": "بستر",
    "wardrobe": "الماری", "cabinet": "کابینہ", "bookshelf": "کتابوں کی الماری",
    "door": "دروازہ", "window": "کھڑکی", "refrigerator": "فریج",
    "microwave": "مائیکرو ویو", "oven": "اوون", "toaster": "ٹوسٹر",
    "washing machine": "واشنگ مشین", "fan": "پنکھا", "air conditioner": "اے سی",
    "television": "ٹیلی ویژن", "monitor": "مانیٹر", "laptop": "لیپ ٹاپ",
    "desktop computer": "ڈیسک ٹاپ کمپیوٹر", "keyboard": "کی بورڈ",
    "computer mouse": "کمپیوٹر ماؤس", "mobile phone": "موبائل فون",
    "tablet": "ٹیبلٹ", "remote control": "ریموٹ کنٹرول", "camera": "کیمرہ",
    "headphones": "ہیڈ فون", "speaker": "اسپیکر", "microphone": "مائیکروفون",
    "printer": "پرنٹر", "watch": "گھڑی", "clock": "گھڑی", "lamp": "لیمپ",
    "light bulb": "بلب", "bottle": "بوتل", "cup": "کپ", "mug": "مگ",
    "glass": "گلاس", "plate": "پلیٹ", "bowl": "پیالہ", "spoon": "چمچ",
    "fork": "کانٹا", "knife": "چھری", "pot": "دیگچی", "pan": "فرائنگ پین",
    "water jug": "پانی کا جگ", "food container": "کھانے کا ڈبہ",
    "backpack": "بیگ", "handbag": "ہینڈ بیگ", "suitcase": "سوٹ کیس",
    "wallet": "بٹوا", "umbrella": "چھتری", "book": "کتاب",
    "notebook": "نوٹ بک", "paper": "کاغذ", "pen": "قلم", "pencil": "پنسل",
    "scissors": "قینچی", "ruler": "فٹہ", "calculator": "کیلکولیٹر",
    "stapler": "اسٹیپلر", "toothbrush": "دانتوں کا برش", "comb": "کنگھی",
    "hair dryer": "ہیئر ڈرائر", "soap bottle": "صابن کی بوتل",
    "shoe": "جوتا", "sandal": "چپل", "shirt": "قمیض", "jacket": "جیکٹ",
    "trousers": "پتلون", "hat": "ٹوپی", "helmet": "ہیلمٹ",
    "glasses": "عینک", "ball": "گیند", "football": "فٹ بال",
    "cat": "بلی", "dog": "کتا", "bird": "پرندہ", "horse": "گھوڑا",
    "cow": "گائے", "sheep": "بھیڑ", "potted plant": "گملے والا پودا",
    "flower": "پھول", "banana": "کیلا", "apple": "سیب",
}

with st.sidebar:
    st.header("⚙️ Detection settings")
    confidence = st.slider("Confidence", 0.10, 0.90, 0.25, 0.05)
    image_size = st.select_slider("Image size (CPU speed)", options=[320, 416, 512, 640, 768], value=416)
    st.caption("Smaller image sizes are generally faster on CPU.")
    voice_language = st.selectbox("Voice language", ["English", "Urdu"])
    st.caption("Voice is spoken automatically after each detection. Urdu requires a compatible Urdu TTS voice installed in Windows.")
    st.divider()
    st.caption(f"Loaded prompt categories: {len(OBJECTS)}")

tab_image, tab_camera, tab_info = st.tabs(["🖼️ Image detection", "📷 Webcam snapshot", "ℹ️ About"])

def show_result(pil_image):
    image_array = np.array(pil_image.convert("RGB"))
    with st.spinner("Detecting objects on CPU… first run may download the model."):
        result = detect(image_array, confidence, image_size)
    annotated = result.plot()
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    st.image(annotated, caption="Detection result", use_container_width=True)

    names = result.names
    counts = Counter(names[int(box.cls[0])] for box in result.boxes) if result.boxes is not None else Counter()
    col1, col2 = st.columns(2)
    col1.metric("Objects detected", sum(counts.values()))
    col2.metric("Different categories", len(counts))
    if counts:
        st.subheader("Detected objects")
        st.dataframe(
            [{"Object": name, "Count": count} for name, count in counts.most_common()],
            use_container_width=True,
            hide_index=True,
        )
        if voice_language == "Urdu":
            spoken_names = [URDU_NAMES.get(name, name) for name, count in counts.most_common()]
            speech_text = "، ".join(spoken_names)
        else:
            speech_text = "I can see " + ", ".join(
                f"{count} {name}" for name, count in counts.most_common()
            )
        st.info(f"🔊 Speaking detected objects in {voice_language} automatically…")
        ok, message = speak(speech_text, voice_language)
        (st.success if ok else st.warning)(message)
    else:
        st.info("No objects detected. Try lowering the confidence setting or using a clearer image.")

with tab_image:
    uploaded = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
    if uploaded:
        image = Image.open(io.BytesIO(uploaded.getvalue())).convert("RGB")
        st.image(image, caption="Input image", use_container_width=True)
        if st.button("🔍 Detect objects", type="primary"):
            show_result(image)

with tab_camera:
    st.write("Take a snapshot using your device camera, then run detection.")
    camera_image = st.camera_input("Camera")
    if camera_image:
        image = Image.open(io.BytesIO(camera_image.getvalue())).convert("RGB")
        if st.button("📷 Detect in snapshot", type="primary"):
            show_result(image)

with tab_info:
    st.subheader("About VisionSpeak")
    st.write("VisionSpeak uses YOLO-World with 100 everyday object prompts. It runs on CPU and does not require an NVIDIA GPU.")
    st.warning("CPU detection is slower than GPU detection. The first run downloads the model. Open-vocabulary detections are estimates and may miss or confuse similar objects.")
    st.write("Speech starts automatically after detection. Urdu speech requires a compatible Urdu voice installed in Windows.")
    with st.expander("Show all 100 object categories"):
        st.write(", ".join(OBJECTS))
