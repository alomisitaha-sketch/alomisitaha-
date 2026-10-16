import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="إحصاء ومقارنة ألفاظ القرآن الكريم", layout="centered")

st.title("📖 تضافر الكلمات والإحصاء القرآني")
st.write("هذا التطبيق يتيح لك مقارنة عدد مرات تكرار أي كلمتين في القرآن الكريم واكتشاف التوافق الإحصائي بدقة.")

# دالة محسنة لجلب البيانات من رابط استضافة مستقر
@st.cache_data
def load_quran():
    # استخدام رابط مستودع مباشر ومفتوح للقرآن الكريم بصيغة JSON
    url = "https://raw.githubusercontent.com/risan/quran-json/main/dist/quran.json"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None
    return None

with st.spinner("جاري تحميل بيانات القرآن الكريم وتجهيز محرك البحث..."):
    quran_data = load_quran()

if quran_data:
    # خانات الإدخال للمستخدم
    col1, col2 = st.columns(2)
    with col1:
        word1 = st.text_input("أدخل الكلمة الأولى:", "الملائكة")
    with col2:
        word2 = st.text_input("أدخل الكلمة الثانية:", "الشياطين")

    # زر المقارنة
    if st.button("إجراء الإحصاء والمقارنة 🔍"):
        if not word1 or not word2:
            st.warning("الرجاء إدخال الكلمتين معاً لإتمام المقارنة.")
        else:
            count1 = 0
            count2 = 0
            matches1 = []
            matches2 = []

            # هيكلية البيانات في هذا الرابط تعتمد على السور والآيات (verses)
            for surah in quran_data:
                surah_name = surah.get('name', '')
                for ayah in surah.get('verses', []):
                    text = ayah.get('text', '')
                    ayah_num = ayah.get('id', '')
                    
                    if word1 in text:
                        c = text.count(word1)
                        count1 += c
                        matches1.append(f"سورة {surah_name} - الآية {ayah_num}")
                        
                    if word2 in text:
                        c = text.count(word2)
                        count2 += c
                        matches2.append(f"سورة {surah_name} - الآية {ayah_num}")

            st.markdown("---")
            st.subheader("📊 نتائج المقارنة الإحصائية:")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric(label=f"تكرار لفظ: ({word1})", value=f"{count1} مرة")
            with col_res2:
                st.metric(label=f"تكرار لفظ: ({word2})", value=f"{count2} مرة")

            if count1 == count2:
                st.success(f"✨ توافق إحصائي تام! الكلمتان متساويتان تماماً ({count1} = {count2}).")
            else:
                diff = abs(count1 - count2)
                st.info(f"الفرق بينهما هو: {diff} مرة.")

            with st.expander(f"عرض الآيات التي وردت فيها كلمة ({word1})"):
                if matches1:
                    for m in matches1:
                        st.write(m)
                else:
                    st.write("لم تُعثر مطابقات دقيقة (تأكد من كتابة الكلمة بدون تشكيل معقد).")

            with st.expander(f"عرض الآيات التي وردت فيها كلمة ({word2})"):
                if matches2:
                    for m in matches2:
                        st.write(m)
                else:
                    st.write("لم تُعثر مطابقات دقيقة.")
else:
    st.error("لم نتمكن من الاتصال بقاعدة البيانات. يرجى التأكد من اتصال الإنترنت أو إعادة تحميل الصفحة (Refresh).")
