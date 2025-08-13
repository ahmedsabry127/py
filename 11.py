import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# إخفاء قائمة الإعدادات و الفوتر
def hide_streamlit_menu():
    hide_menu = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)

# تهيئة Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

# واجهة مدير الملفات
def file_manager(db):
    st.subheader("📁 مدير الملفات")
    st.write("يمكنك إنشاء مجلدات وملفات (روابط).")

    folder_name = st.text_input("اسم المجلد")
    if st.button("إنشاء مجلد"):
        if folder_name:
            try:
                db.collection("file_manager").add({"type": "folder", "name": folder_name})
                st.success(f"تم إنشاء المجلد '{folder_name}' بنجاح ✅")
            except Exception as e:
                st.error(f"خطأ: {e}")
        else:
            st.warning("⚠ الرجاء إدخال اسم المجلد.")

    file_name = st.text_input("اسم الملف")
    file_link = st.text_input("رابط الملف")
    if st.button("إنشاء ملف"):
        if file_name and file_link:
            try:
                db.collection("file_manager").add({"type": "file", "name": file_name, "link": file_link})
                st.success(f"تم إنشاء الملف '{file_name}' بنجاح ✅")
            except Exception as e:
                st.error(f"خطأ: {e}")
        else:
            st.warning("⚠ الرجاء إدخال اسم الملف والرابط.")

    st.subheader("📂 الملفات والمجلدات")
    try:
        docs = db.collection("file_manager").stream()
        for doc in docs:
            data = doc.to_dict()
            if data["type"] == "folder":
                st.write(f"📁 {data['name']}")
            elif data["type"] == "file":
                st.write(f"📄 [{data['name']}]({data['link']})")
    except Exception as e:
        st.error(f"خطأ: {e}")

# صفحة التسجيل
def registration_page(db):
    st.subheader("📋 إنشاء حساب جديد")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("تسجيل"):
        try:
            user = auth.create_user(email=email, password=password)
            st.success(f"تم إنشاء الحساب بنجاح ✅ - UID: {user.uid}")
            st.session_state["authenticated"] = True  # Set authentication state
            st.experimental_rerun()  # Reload the app to show the file manager
        except Exception as e:
            st.error(f"خطأ: {e}")

# صفحة تسجيل الدخول
def login_page(db):
    st.subheader("🔑 تسجيل الدخول")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("دخول"):
        st.warning("⚠ تسجيل الدخول بكلمة المرور غير مدعوم مباشرة عبر Admin SDK.\n"
                   "هنا يمكننا فقط التحقق من وجود المستخدم.")
        try:
            user = auth.get_user_by_email(email)
            st.success(f"تم العثور على الحساب ✅ - UID: {user.uid}")
            st.session_state["authenticated"] = True  # Set authentication state
            st.experimental_rerun()  # Reload the app to show the file manager
        except Exception as e:
            st.error(f"خطأ: {e}")

# التطبيق الرئيسي
def main():
    hide_streamlit_menu()
    db = initialize_firebase()

    st.title("🔐 تسجيل الدخول عبر Firebase")

    # تحقق من حالة المصادقة
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        file_manager(db)  # Show file manager if authenticated
    else:
        page = st.sidebar.radio("اختر الصفحة", ["تسجيل", "دخول"])
        if page == "تسجيل":
            registration_page(db)
        elif page == "دخول":
            login_page(db)

if __name__ == "__main__":
    main()
