import streamlit as st
import jdatetime

# --- تنظیمات کلی اپلیکیشن ---
st.set_page_config(page_title="سیستم ردیابی تولید تسلا", page_icon="⚡", layout="wide")

# --- تزریق CSS و فونت مدرن Vazirmatn ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700;900&display=swap');

    body, p, div, input, select, label, textarea, button, span { 
        direction: rtl; 
        text-align: right !important; 
        font-family: 'Vazirmatn', Tahoma, sans-serif !important; 
    }
    h1 { font-weight: 900 !important; text-align: center; color: #1565C0; margin-bottom: 20px; }
    h2, h3 { font-weight: 700 !important; text-align: center; color: #1E88E5; }
    .stTextInput>div>div>input { text-align: right; }
    .stSelectbox>div>div>div { text-align: right; }
    .stMultiSelect>div>div>div { direction: rtl; text-align: right; }

    .qc-header { color: #D84315; font-weight: 900; margin-top: 15px; font-size: 1.1em; border-bottom: 2px solid #FFCCBC; padding-bottom: 5px; }
    .date-label { font-size: 14px; font-weight: 700; margin-bottom: -15px; color: #424242; }

    /* استایل تایم‌لاین */
    .timeline-container { border-right: 4px solid #1E88E5; padding-right: 20px; margin-right: 15px; margin-top: 10px; }
    .timeline-item { margin-bottom: 25px; padding: 15px; background-color: #f8f9fa; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); position: relative; }
    .timeline-item::before { content: ''; position: absolute; width: 16px; height: 16px; background-color: #1E88E5; border-radius: 50%; right: -30px; top: 15px; }
    .timeline-date { color: #43A047; font-weight: 900; font-size: 1.1em; margin-bottom: 8px; }
    .timeline-detail { margin: 5px 0; font-size: 0.95em; }

    /* استایل باکس‌های خلاصه */
    .summary-card { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 4px solid; height: 100%; }
    .card-title { font-weight: 900; font-size: 1.2em; margin-bottom: 15px; }
    .card-item { margin-bottom: 8px; font-size: 0.95em; }
    .card-item strong { color: #333; }
    </style>
""", unsafe_allow_html=True)

# --- منوی کناری (Sidebar) ---
st.sidebar.title("⚡ سیستم تسلا")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("منوی اصلی:", ["📝 ثبت اطلاعات تولید", "📊 پنل مدیریت و رهگیری"])
st.sidebar.markdown("---")
st.sidebar.info("نسخه دمو (بدون اتصال به دیتابیس)")

# =====================================================================
# صفحه اول: ثبت اطلاعات تولید
# =====================================================================
if app_mode == "📝 ثبت اطلاعات تولید":
    st.title("🏭 فرم ثبت لاگ تولید")
    st.markdown("---")

    today_jdate = jdatetime.date.today()
    today_shamsi = today_jdate.strftime("%Y/%m/%d")
    st.caption(f"📅 تاریخ امروز: {today_shamsi}")


    def shamsi_date_picker(label_text, key_prefix):
        st.markdown(f"<p class='date-label'>{label_text}</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1.5])
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = ["۰۱ فروردین", "۰۲ اردیبهشت", "۰۳ خرداد", "۰۴ تیر", "۰۵ مرداد", "۰۶ شهریور", "۰۷ مهر", "۰۸ آبان",
                  "۰۹ آذر", "۱۰ دی", "۱۱ بهمن", "۱۲ اسفند"]
        years = [str(i) for i in range(1402, 1410)]
        with c1: day = st.selectbox("روز", days, index=today_jdate.day - 1, key=f"{key_prefix}_day")
        with c2: month = st.selectbox("ماه", months, index=today_jdate.month - 1, key=f"{key_prefix}_month")
        with c3: year = st.selectbox("سال", years, index=years.index(str(today_jdate.year)), key=f"{key_prefix}_year")
        month_num = month.split(" ")[0]
        return f"{year}/{month_num}/{day}"


    col1, col2 = st.columns(2)
    with col1:
        serial_number = st.text_input("شماره سریال دستگاه:", placeholder="مثال: PE2025TS016")
    with col2:
        technicians = st.multiselect("تکنسین(ها):", ["مهدی نجاتیان", "سجاد محبی", "محمد سعید کبیری", "پرسنل موقت"])

    st.markdown("---")
    st.subheader("بخشی که روی آن کار کرده‌اید را انتخاب کنید:")
    department = st.selectbox("", ["📌 یک بخش را انتخاب کنید...", "۱. باکس الکترونیک", "۲. استند", "۳. سیت", "۴. هندل",
                                   "۵. کنترل کیفیت (QC)", "۶. تعمیرات", "۷. مشخصات مشتری"])

    form_data = {}

    if department != "📌 یک بخش را انتخاب کنید...":
        # ... (کدهای بخش فرم تولید دقیقاً مشابه نسخه قبلی است، برای جلوگیری از طولانی شدن مخفی شده‌اند)
        if department == "۱. باکس الکترونیک":
            tasks_mech = st.multiselect("مکانیک و بدنه:",
                                        ["بستن قسمت L شکل", "جایگاه منابع", "جایگاه خازن", "بستن فن ها و گارد",
                                         "زدن پرچی بدنه", "نصب قطعات (رله، ترمینال)"])
            tasks_boards = st.multiselect("مونتاژ بردها و قدرت:",
                                          ["مونتاژ برد پاور", "مونتاژ برد دیجیتال", "مونتاژ برد رکتیفایر",
                                           "مجموعه خازن، دیود و تریستور"])
            if any(b in tasks_boards for b in ["مونتاژ برد پاور", "مونتاژ برد دیجیتال", "مونتاژ برد رکتیفایر"]):
                st.warning("⚠️ فعالیت شما نیاز به ثبت سریال دارد:")
                c_b1, c_b2, c_b3 = st.columns(3)
                if "مونتاژ برد پاور" in tasks_boards: form_data["سریال برد پاور"] = c_b1.text_input("سریال برد پاور:")
                if "مونتاژ برد دیجیتال" in tasks_boards: form_data["سریال برد دیجیتال"] = c_b2.text_input(
                    "سریال برد دیجیتال:")
                if "مونتاژ برد رکتیفایر" in tasks_boards: form_data["سریال رکتیفایر"] = c_b3.text_input(
                    "سریال رکتیفایر:")
            form_data["فعالیت مکانیک"] = tasks_mech;
            form_data["فعالیت بردها"] = tasks_boards

        elif department == "۷. مشخصات مشتری":
            form_data["مشتری"] = st.text_input("نام مشتری:");
            form_data["تاریخ خروج"] = shamsi_date_picker("تاریخ خروج:", "deliv")

        st.markdown("---")
        if st.button("💾 ثبت لاگ تولید", use_container_width=True):
            if not serial_number or not technicians:
                st.error("❌ 'شماره سریال' و 'نام تکنسین(ها)' الزامی است.")
            else:
                st.success("✅ ثبت با موفقیت انجام شد!")

# =====================================================================
# صفحه دوم: پنل مدیریت و تاریخچه
# =====================================================================
elif app_mode == "📊 پنل مدیریت و رهگیری":
    st.title("📊 پنل مدیریت: داشبورد وضعیت دستگاه")
    st.write("با وارد کردن شماره سریال دستگاه، خلاصه‌ی اطلاعات حیاتی و ریزِ تاریخچه تولید آن را مشاهده کنید.")
    st.markdown("---")

    # بخش جستجو
    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
    with search_col1:
        search_query = st.text_input("🔍 جستجوی شماره سریال دستگاه:", placeholder="مثلا PE2025TS016 را تایپ کنید...")
    with search_col2:
        st.write("")
        st.write("")
        search_btn = st.button("جستجوی اطلاعات", use_container_width=True)

    # نمایش نتایج جستجو
    if search_btn:
        if search_query:
            st.success(f"نتایج یافت شده برای دستگاه: **{search_query}**")

            # --- بخش اول: خلاصه اطلاعات حیاتی (Cards) ---
            st.markdown("### 📋 خلاصه وضعیت دستگاه")

            # استفاده از کدهای HTML/CSS برای ساخت کارت‌های زیبا
            st.markdown("""
            <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px;">
                <!-- کارت مشخصات مشتری -->
                <div class="summary-card" style="flex: 1; min-width: 250px; border-top-color: #4CAF50;">
                    <div class="card-title" style="color: #4CAF50;">🏢 اطلاعات مشتری</div>
                    <div class="card-item"><strong>نام مرکز:</strong> کلینیک فیزیوتراپی توان</div>
                    <div class="card-item"><strong>تلفن:</strong> ۰۲۱-۸۸۸۸۸۸۸۸</div>
                    <div class="card-item"><strong>تاریخ تحویل:</strong> ۱۴۰۳/۰۶/۲۵</div>
                    <div class="card-item"><strong>وضعیت گارانتی:</strong> فعال 🟢</div>
                </div>

                <!-- کارت سریال قطعات -->
                <div class="summary-card" style="flex: 1; min-width: 250px; border-top-color: #2196F3;">
                    <div class="card-title" style="color: #2196F3;">⚙️ سریال ماژول‌های حیاتی</div>
                    <div class="card-item"><strong>برد پاور:</strong> BP-10023</div>
                    <div class="card-item"><strong>برد دیجیتال:</strong> BD-9941</div>
                    <div class="card-item"><strong>سریال سیت:</strong> ST-4509</div>
                    <div class="card-item"><strong>سریال هندل:</strong> ندارد</div>
                </div>

                <!-- کارت وضعیت QC -->
                <div class="summary-card" style="flex: 1; min-width: 250px; border-top-color: #FF9800;">
                    <div class="card-title" style="color: #FF9800;">🛡️ کنترل کیفیت (QC)</div>
                    <div class="card-item"><strong>دفعات تست نهایی:</strong> ۳ بار (۲۰ دقیقه‌ای)</div>
                    <div class="card-item"><strong>تست خط و خش:</strong> تایید شده ✔️</div>
                    <div class="card-item"><strong>وضعیت نهایی:</strong> <span style="color:green; font-weight:bold;">مجوز خروج (Pass) ✅</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- بخش دوم: جزئیات تاریخچه تولید (پنهان شده در Expander) ---
            st.markdown("### 🔍 لاگ کامل خط تولید")
            with st.expander("نمایش ریزِ تاریخچه تولید (چه کسی، چه کاری، در چه زمانی انجام داده است؟)"):

                st.markdown(f"""
                <div class="timeline-container">
                    <div class="timeline-item">
                        <div class="timeline-date">🟢 ۱۴۰۳/۰۶/۱۵ - ۱۰:۳۰ صبح</div>
                        <div class="timeline-detail"><b>👤 تیم تکنسین:</b> سجاد محبی، مهدی نجاتیان</div>
                        <div class="timeline-detail"><b>🏭 دپارتمان:</b> ۱. باکس الکترونیک</div>
                        <div class="timeline-detail" style="color: #555;">
                            <b>جزئیات فعالیت:</b> بستن قسمت L شکل، مونتاژ برد پاور.<br>
                        </div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-date">🟢 ۱۴۰۳/۰۶/۱۶ - ۱۴:۱۵ ظهر</div>
                        <div class="timeline-detail"><b>👤 تیم تکنسین:</b> محمد سعید کبیری</div>
                        <div class="timeline-detail"><b>🏭 دپارتمان:</b> ۵. کنترل کیفیت (QC)</div>
                        <div class="timeline-detail" style="color: #555;">
                            <b>جزئیات فعالیت:</b> حین تولید - تست جریان کشی (تایید ✔️).
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ لطفا ابتدا یک شماره سریال برای جستجو وارد کنید.")