import streamlit as st
import re

st.markdown("""
<style>
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(-45deg, #050816, #0b1b3a, #1a0f2e, #000000);
    background-size: 400% 400%;
    animation: bgShift 18s ease infinite;
}
[data-testid="stAppViewContainer"] > .main > div:first-child {
    padding-bottom: 240px;
}
[data-testid="stBlock"] {
    position: relative;
    z-index: 10;
}
@keyframes bgShift {
    0%  { background-position: 0%   50%; }
    50% { background-position: 100% 50%; }
    100%{ background-position: 0%   50%; }
}
@keyframes moveTrain {
    0%   { transform: translateX(-220px); }
    100% { transform: translateX(110vw); }
}
@keyframes fall {
    0%   { transform: translateY(0) translateX(0) rotate(0deg); opacity: 1; }
    90%  { opacity: .85; }
    100% { transform: translateY(120vh) translateX(80px) rotate(360deg); opacity: .70; }
}
@keyframes twinkle {
    0%, 90% { opacity: .3; }
    80%       { opacity: .2; }
}

/* ── Scene container ── */
.jp {
    position: fixed;
    inset: 0;          /* replaces top/left/right/bottom */
    width: 100%;
    height: 100vh;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

/* ── Ground ── */
.jp-ground {
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 80px;
    background: #080f1e;
}

/* ── Track lines ── */
.jp-track {
    position: absolute;
    left: 0; width: 100%; height: 3px;
    background: #2a3550;
}

.jp-fuji {
    position: absolute;
    bottom: 70px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
}

/* Main mountain body (wider, more natural slope) */
.jp-fuji::before {
    content: "";
    position: absolute;
    left: -210px;
    bottom: 0;
    width: 0;
    height: 0;
    border-left: 210px solid transparent;
    border-right: 210px solid transparent;
    border-bottom: 200px solid #1a1a2a;
    opacity: 0.95;
}

/* Snow cap (smaller, centered, more realistic peak) */
.jp-fuji::after {
    content: "";
    position: absolute;
    left: -85px;
    bottom: 120px;
    width: 0;
    height: 0;
    border-left: 85px solid transparent;
    border-right: 85px solid transparent;
    border-bottom: 80px solid #e6eef7;
    opacity: 0.8;
}

/* ── Buildings ── */
.jp-bld {
    position: absolute;
    bottom: 78px;
    background: #0d1525;
}

/* ── Window lights ── */
.jp-win-l {
    position: absolute;
    width: 8px; height: 5px;
    background: rgba(255,224,128,.6);
    border-radius: 1px;
}

/* ── Cherry tree trunk ── */
.jp-trunk {
    position: absolute;
    bottom: 78px;
    width: 9px;
    background: #1a0a0f;
}
/* ── Cherry blossom blob ── */
.jp-blob {
    position: absolute;
    background: #6b2040;
    border-radius: 50%;
}

/* ── Stars ── */

.jp-star {
    position: absolute;

    /* softer, less bright colors */
    background: linear-gradient(45deg, #f6f8ff, #b9cbe6);

    clip-path: polygon(
        50% 0%,
        61% 35%,
        98% 35%,
        68% 57%,
        79% 91%,
        50% 70%,
        21% 91%,
        32% 57%,
        2% 35%,
        39% 35%
    );

    /* more subtle presence */
    opacity: 0.35;

    /* lighter glow */
    filter: drop-shadow(0 0 3px rgba(160, 200, 255, 0.25));

    transform: rotate(10deg);

    /* keep both animations in one declaration */
    animation: twinkle 4.5s ease-in-out infinite, drift 25s linear infinite;
}
/* ── Moon ── */
.jp-moon {
    position: absolute;
    top: 12px; right: 7%;
    width: 80px; height: 80px;
    background: #fff8d0;
    border-radius: 50%;
    box-shadow: 0 0 180px rgba(255,240,180,.95);
}

/* ── Train ── */
.jp-train {
    position: absolute;
    bottom: 96px; left: 0;
    width: 160px; height: 24px;
    background: #e8eaf0;
    border-radius: 6px 14px 14px 6px;
    animation: moveTrain 45s linear infinite;
    box-shadow: 10 10 6px rgba(200,220,255,.5);
}
.jp-car::before {     content: "";
    position: absolute;
    right: -1px;
    top: 12px;
    width: 9px;
    height: 7px;
    background: #fff3a0;
    border-radius: 50%;
    box-shadow: 18px 10px 28px 8px rgba(190, 240, 160, 0.45);
}
.jp-train::after {display: none;
}
.jp-car {
    border-radius: 30px;
}
.jp-win {
    position: absolute;
    top: 7px;
    width: 16px; height: 9px;
    background: rgba(80,230,200,.85);
    border-radius: 3px;
}

/* ── Petals ── */
.jp-petal {
    position: absolute;
    top: -12px;

    width: 14px;
    height: 14px;

    background: radial-gradient(circle at 30% 30%, #ffd1dc, #ff7f9c 65%, #ff4f7a);
    border-radius: 80% 90% 70% 40%;

    opacity: 0.85;

    filter: drop-shadow(0 8px 8px rgba(255, 90, 130, 0.35));

    animation: fall 14s linear infinite, sway 30s ease-in-out infinite;

    transform-origin: center;
}
/* size + opacity variation */
.jp-petal:nth-child(3n) {
    width: 10px;
    height: 10px;
    opacity: 0.65;
}

.jp-petal:nth-child(4n) {
    width: 18px;
    height: 18px;
    opacity: 0.9;
}

.jp-petal:nth-child(5n) {
    width: 22px;
    height: 22px;
    opacity: 0.75;
}
.jp-petal:nth-child(2n) {
    animation-duration: 6s, 3s;
}

.jp-petal:nth-child(3n) {
    animation-duration: 10s, 5s;
}

.jp-petal:nth-child(5n) {
    animation-duration: 12s, 6s;
}

</style>

<div class="jp">

  <!-- Moon -->
  <div class="jp-moon"></div>

<!-- Stars (rebalanced + expanded) -->
<div class="jp-star" style="width:6px;height:6px;top:6%;left:6%;animation-duration:2.2s"></div>
<div class="jp-star" style="width:8px;height:8px;top:10%;left:18%;animation-duration:3.4s"></div>
<div class="jp-star" style="width:7px;height:7px;top:4%;left:32%;animation-duration:2.7s"></div>
<div class="jp-star" style="width:10px;height:10px;top:14%;left:44%;animation-duration:1.9s"></div>
<div class="jp-star" style="width:6px;height:6px;top:7%;left:58%;animation-duration:3.1s"></div>
<div class="jp-star" style="width:11px;height:11px;top:3%;left:72%;animation-duration:2.4s"></div>
<div class="jp-star" style="width:8px;height:8px;top:16%;left:86%;animation-duration:3.8s"></div>
<div class="jp-star" style="width:5px;height:5px;top:22%;left:12%;animation-duration:2.9s"></div>
<div class="jp-star" style="width:7px;height:7px;top:24%;left:28%;animation-duration:2.3s"></div>
<div class="jp-star" style="width:6px;height:6px;top:21%;left:52%;animation-duration:3.6s"></div>
<div class="jp-star" style="width:9px;height:9px;top:26%;left:66%;animation-duration:2.1s"></div>
<div class="jp-star" style="width:6px;height:6px;top:23%;left:80%;animation-duration:3.0s"></div>

  <!-- Fuji -->
  <div class="jp-fuji"></div>

  <!-- Buildings left -->
  <div class="jp-bld" style="left:5%;  width:4%; height:95px; background:#0d1525;"></div>
  <div class="jp-bld" style="left:10%; width:5%; height:75px; background:#0b1220;"></div>
  <div class="jp-bld" style="left:16%; width:3%; height:108px;background:#0d1828;"></div>
  <div class="jp-bld" style="left:20%; width:6%; height:62px; background:#0b1220;"></div>
  <div class="jp-bld" style="left:27%; width:4%; height:80px; background:#0d1525;"></div>
  <div class="jp-bld" style="left:32%; width:3%; height:55px; background:#0b1220;"></div>

  <!-- Buildings right -->
  <div class="jp-bld" style="right:5%;  width:4%; height:90px; background:#0d1525;"></div>
  <div class="jp-bld" style="right:10%; width:5%; height:70px; background:#0b1220;"></div>
  <div class="jp-bld" style="right:16%; width:3%; height:105px;background:#0d1828;"></div>
  <div class="jp-bld" style="right:20%; width:6%; height:60px; background:#0b1220;"></div>
  <div class="jp-bld" style="right:27%; width:4%; height:78px; background:#0d1525;"></div>
  <div class="jp-bld" style="right:32%; width:3%; height:52px; background:#0b1220;"></div>

  <!-- Buildings left -->
  <div class="jp-bld" style="left:5%;  width:4%; height:95px; background:#0d1525;"></div>
  <div class="jp-bld" style="left:10%; width:5%; height:75px; background:#0b1220;"></div>
  <div class="jp-bld" style="left:16%; width:3%; height:108px;background:#0d1828;"></div>
  <div class="jp-bld" style="left:20%; width:6%; height:62px; background:#0b1220;"></div>
  <div class="jp-bld" style="left:27%; width:4%; height:80px; background:#0d1525;"></div>
  <div class="jp-bld" style="left:32%; width:3%; height:55px; background:#0b1220;"></div>

  <!-- Window lights left -->
  <div class="jp-win-l" style="left:5.6%;  bottom:140px;"></div>
  <div class="jp-win-l" style="left:6.6%;  bottom:140px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="left:5.6%;  bottom:128px;"></div>
  <div class="jp-win-l" style="left:6.6%;  bottom:128px;"></div>

  <div class="jp-win-l" style="left:10.6%; bottom:128px;"></div>
  <div class="jp-win-l" style="left:11.8%; bottom:128px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="left:10.6%; bottom:116px;"></div>

  <div class="jp-win-l" style="left:16.4%; bottom:150px;"></div>
  <div class="jp-win-l" style="left:17.4%; bottom:150px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="left:16.4%; bottom:138px;"></div>
  <div class="jp-win-l" style="left:17.4%; bottom:138px;"></div>

  <div class="jp-win-l" style="left:20.6%; bottom:118px;"></div>
  <div class="jp-win-l" style="left:21.8%; bottom:118px;"></div>
  <div class="jp-win-l" style="left:23.0%; bottom:118px; background:rgba(128,192,255,.5);"></div>

  <div class="jp-win-l" style="left:27.6%; bottom:132px;"></div>
  <div class="jp-win-l" style="left:28.8%; bottom:132px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="left:27.6%; bottom:120px;"></div>

  <!-- Buildings right -->
  <div class="jp-bld" style="right:5%;  width:4%; height:90px; background:#0d1525;"></div>
  <div class="jp-bld" style="right:10%; width:5%; height:70px; background:#0b1220;"></div>
  <div class="jp-bld" style="right:16%; width:3%; height:105px;background:#0d1828;"></div>
  <div class="jp-bld" style="right:20%; width:6%; height:60px; background:#0b1220;"></div>
  <div class="jp-bld" style="right:27%; width:4%; height:78px; background:#0d1525;"></div>
  <div class="jp-bld" style="right:32%; width:3%; height:52px; background:#0b1220;"></div>

  <!-- Window lights right -->
  <div class="jp-win-l" style="right:5.6%;  bottom:138px;"></div>
  <div class="jp-win-l" style="right:6.6%;  bottom:138px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="right:5.6%;  bottom:126px;"></div>
  <div class="jp-win-l" style="right:6.6%;  bottom:126px;"></div>

  <div class="jp-win-l" style="right:10.6%; bottom:122px;"></div>
  <div class="jp-win-l" style="right:11.8%; bottom:122px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="right:10.6%; bottom:110px;"></div>

  <div class="jp-win-l" style="right:16.4%; bottom:148px;"></div>
  <div class="jp-win-l" style="right:17.4%; bottom:148px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="right:16.4%; bottom:136px;"></div>
  <div class="jp-win-l" style="right:17.4%; bottom:136px;"></div>

  <div class="jp-win-l" style="right:20.6%; bottom:116px;"></div>
  <div class="jp-win-l" style="right:21.8%; bottom:116px;"></div>
  <div class="jp-win-l" style="right:23.0%; bottom:116px; background:rgba(128,192,255,.5);"></div>

  <div class="jp-win-l" style="right:27.6%; bottom:130px;"></div>
  <div class="jp-win-l" style="right:28.8%; bottom:130px; background:rgba(128,192,255,.5);"></div>
  <div class="jp-win-l" style="right:27.6%; bottom:118px;"></div>

  <!-- Cherry trees left -->
  <div class="jp-trunk" style="left:2%; height:90px;"></div>
  <div class="jp-blob"  style="bottom:145px;left:0.5%;width:70px;height:52px;opacity:.75;"></div>
  <div class="jp-blob"  style="bottom:132px;left:0%;  width:44px;height:36px;background:#7d2850;opacity:.6;"></div>

  <div class="jp-trunk" style="left:7%; height:75px;"></div>
  <div class="jp-blob"  style="bottom:140px;left:5.5%;width:56px;height:44px;opacity:.7;"></div>

  <!-- Cherry trees right -->
  <div class="jp-trunk" style="right:2%; height:90px;"></div>
  <div class="jp-blob"  style="bottom:145px;right:0.5%;width:70px;height:52px;opacity:.75;"></div>
  <div class="jp-blob"  style="bottom:132px;right:0%;  width:44px;height:36px;background:#7d2850;opacity:.6;"></div>

  <div class="jp-trunk" style="right:7%; height:75px;"></div>
  <div class="jp-blob"  style="bottom:140px;right:5.5%;width:56px;height:44px;opacity:.7;"></div>

  <!-- Ground -->
  <div class="jp-ground"></div>

  <!-- Tracks -->
  <div class="jp-track" style="bottom:87px;"></div>
  <div class="jp-track" style="bottom:81px;"></div>

  <!-- Train -->
  <div class="jp-train">
    <div class="jp-win" style="left:26px"></div>
    <div class="jp-win" style="left:52px"></div>
    <div class="jp-win" style="left:78px"></div>
    <div class="jp-win" style="left:104px"></div>
  </div>

  <!-- Train car 1 (engine) -->
  <div class="jp-train" style="animation-delay: 0s;">
    <div class="jp-win" style="left:26px"></div>
    <div class="jp-win" style="left:52px"></div>
    <div class="jp-win" style="left:78px"></div>
    <div class="jp-win" style="left:104px"></div>
  </div>

  <!-- Train car 2 -->
  <div class="jp-train" style="animation-delay: -2.5s;">
    <div class="jp-win" style="left:26px"></div>
    <div class="jp-win" style="left:52px"></div>
    <div class="jp-win" style="left:78px"></div>
    <div class="jp-win" style="left:104px"></div>
  </div>

  <!-- Train car 3 -->
  <div class="jp-train jp-car" style="animation-delay: -5s;">
    <div class="jp-win" style="left:26px"></div>
    <div class="jp-win" style="left:52px"></div>
    <div class="jp-win" style="left:78px"></div>
    <div class="jp-win" style="left:104px"></div>
  </div>

  <!-- Petals -->
  <div class="jp-petal" style="left:8%;  animation-duration:29s; animation-delay:0s;"></div>
  <div class="jp-petal" style="left:20%; animation-duration:37s; animation-delay:2s;"></div>
  <div class="jp-petal" style="left:35%; animation-duration:34s; animation-delay:5s;"></div>
  <div class="jp-petal" style="left:50%; animation-duration:28s; animation-delay:1s;"></div>
  <div class="jp-petal" style="left:65%; animation-duration:36s; animation-delay:8s;"></div>
  <div class="jp-petal" style="left:80%; animation-duration:32s; animation-delay:3s;"></div>
  <div class="jp-petal" style="left:93%; animation-duration:40s; animation-delay:6s;"></div>

</div>
""", unsafe_allow_html=True)


# ── App ──────────────────────────────────────────────────────────────────────
st.title("Parcel Number Formatter")

def remove_dashes(value):
    return re.sub(r"[^0-9A-Z]", "", str(value))

def add_dashes(value):
    digits = remove_dashes(value)
    if len(digits) != 10:
        return f"{digits[:2]}-{digits[2:5]}-{digits[5]}-{digits[6:10]}-{digits[10:]}"
    return f"{digits[:2]}-{digits[2:5]}-{digits[5]}-{digits[6:]}"

mode = st.radio("Select Mode", ["Remove Dashes", "Add Dashes", "Strings to List"], key="mode")

if "prev_mode" not in st.session_state:
    st.session_state.prev_mode = st.session_state.mode

if st.session_state.mode != st.session_state.prev_mode:
    st.session_state.parcel_input = ""
    st.session_state.prev_mode = st.session_state.mode
    st.rerun()

if st.button("Reset / Clear"):
    st.session_state.parcel_input = ""
    st.rerun()

if mode == "Remove Dashes":
    user_input = st.text_area("Enter Parcel Numbers (one per line)", key="parcel_input")
    if user_input:
        st.code("\n".join([remove_dashes(x) for x in user_input.splitlines()]))

elif mode == "Add Dashes":
    user_input = st.text_area("Enter Parcel Numbers (one per line)", key="parcel_input")
    if user_input:
        st.code("\n".join([add_dashes(x) for x in user_input.splitlines()]))

elif mode == "Strings to List":
    user_input = st.text_area("Enter Parcel Numbers (one per line)", key="parcel_input")
    if user_input:
        st.code(",\n".join([f"'{add_dashes(x)}'" for x in user_input.splitlines()]))
