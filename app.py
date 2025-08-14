import yt_dlp
import streamlit as st

st.set_page_config(page_title="Video Stream Extractor", page_icon="🎥")

st.title("🎥 Video/Audio Stream Extractor")
st.write("ادخل أى رابط فيديو من YouTube أو أى موقع مدعوم لاستخراج روابط البث المباشر")

url = st.text_input("🌐 رابط الفيديو:")

if st.button("📡 استخراج الروابط"):
    if url.strip():
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'nocheckcertificate': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [info])

                # فلترة الروابط التى تحتوى على صوت + فيديو معًا
                av_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']

                # ترتيب حسب الجودة (height) أو bitrate
                av_formats.sort(key=lambda f: (f.get('height') or 0, f.get('tbr') or 0), reverse=True)

                # عرض الرابط الأفضل أولًا
                if av_formats:
                    best = av_formats[0]
                    st.subheader("🌟 أفضل رابط (صوت + فيديو):")
                    st.markdown(f"**جودة:** {best.get('format_note', 'N/A')}  |  "
                                f"**Codec:** {best.get('vcodec', 'N/A')}  |  "
                                f"**Audio:** {best.get('acodec', 'N/A')}")
                    st.write(f"🔗 [رابط مباشر]({best.get('url')})")
                    st.write("---")

                # عرض كل الروابط الأخرى
                st.subheader("📜 كل الروابط المتاحة:")
                for f in formats:
                    st.markdown(f"**جودة:** {f.get('format_note', 'N/A')}  |  "
                                f"**Codec:** {f.get('vcodec', 'N/A')}  |  "
                                f"**Audio:** {f.get('acodec', 'N/A')}")
                    st.write(f"🔗 [رابط مباشر]({f.get('url')})")
                    st.write("---")

        except Exception as e:
            st.error(f"حدث خطأ: {e}")
    else:
        st.warning("من فضلك أدخل رابط صحيح.")
