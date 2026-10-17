import streamlit as st
import requests

# إعدادات الصفحة
st.set_page_config(page_title="معرفة ألفاظ القرآن الكريم", layout="centered")

st.title("📖 إضافة الكلمات والإحصاء القرآني")
st.write("البحث عن كلمتين في القرآن الكريم والتوافق الإحصائي الدقيق.")

# دالة لجلب البيانات وتخزينها مؤقتاً
@st.cache_data
def load_quran():
    # رابط مباشر لملف JSON القرآني على جيت هاب
    url = "https://raw.githubusercontent.com/alomisitaha-sketch/alomisitaha-/main/quran.json"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"خطأ في الخادم (HTTP Error): {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"حدث خطأ في الاتصال بالشبكة: {e}")
        return None

# تحميل بيانات القرآن
quran_data = load_quran()

if quran_data:
    # خانات إدخال الكلمات
    col1, col2 = st.columns(2)
    with col1:
        word1 = st.text_input("أدخل الكلمة الأولى:")
    with col2:
        word2 = st.text_input("أدخل الكلمة الثانية:")

    if st.button("إجراء الإحصاء والمقارنة 🔍"):
        if not word1 or not word2:
            st.warning("الرجاء إدخال الكلمتين معاً لإجراء المقارنة.")
        else:
            count1 = 0
            count2 = 0
            matches1 = []
            matches2 = []

            # البحث والتجميع في جميع السور والآيات
            for surah in quran_data:
                surah_name = surah.get('name', '')
                for ayah in surah.get('verses', []):
                    text = ayah.get('text', '')
                    ayah_num = ayah.get('id', '')

                    if word1 in text:
                        c = text.count(word1)
                        count1 += c
                        matches1.append(f"سورة {surah_name} - الآية ({ayah_num}): {text}")

                    if word2 in text:
                        c = text.count(word2)
                        count2 += c
                        matches2.append(f"سورة {surah_name} - الآية ({ayah_num}): {text}")

            # عرض النتائج الإحصائية
            st.markdown("---")
            st.subheader("📊 نتائج المقارنة الإحصائية:")

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric(label=f"تكرار لفظ '{word1}'", value=count1)
            with col_res2:
                st.metric(label=f"تكرار لفظ '{word2}'", value=count2)

            if count1 == count2:
                st.success("✨ الكلمتان متساويتان تماماً في عدد التكرارات!")
            else:
                diff = abs(count1 - count2)
                st.info(f"الفرق بينهما هو: {diff} مرة")

            # عرض تفاصيل الآيات للكلمة الأولى
            with st.expander(f"الآيات التي وردت فيها كلمة '{word1}' ({len(matches1)} آية)"):
                if matches1:
                    for m in matches1:
                        st.write(m)
                else:
                    st.write("لم يتم العثور على مطابقات.")

            # عرض تفاصيل الآيات للكلمة الثانية
            with st.expander(f"الآيات التي وردت فيها كلمة '{word2}' ({len(matches2)} آية)"):
                if matches2:
                    for m in matches2:
                        st.write(m)
                else:
                    st.write("لم يتم العثور على مطابقات.")
else:
    st.error("تعذر تحميل بيانات القرآن الكريم. تأكد من وجود ملف quran.json في المستودع.")
 
