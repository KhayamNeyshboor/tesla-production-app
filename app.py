import streamlit as st
import jdatetime

# --- تنظیمات کلی اپلیکیشن ---
st.set_page_config(page_title="سیستم ردیابی تولید تسلا", page_icon="⚡", layout="wide")

# --- تزریق CSS اصلاح شده برای رفع خطوط اضافی سایدبار ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700;900&display=swap');

    /* اعمال فونت به کل برنامه */
    * {
        font-family: 'Vazirmatn', Tahoma, sans-serif !important;
    }

    /* راست‌چین کردن اصولی کل اپلیکیشن */
    .stApp {
        direction: rtl;
    }

    p, input, select, label, textarea, button, span, summary, li { 
        text-align: right !important; 
    }

    /* --------------------------------------------------- */
    /* حل مشکل به هم ریختگی حروف سایدبار و حذف خطوط اضافی */
    [data-testid="stSidebar"][aria-expanded="false"] * {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        border: none !important; /* حذف خط عمودی اضافی */
    }
    /* --------------------------------------------------- */

    /* مستثنی کردن آیکون‌های استریم‌لیت برای جلوگیری از مخدوش شدن */
    .material-symbols-rounded, .material-icons, span[class*="Icon"], [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    /* استایل تیترها */
    h1 { font-weight: 900 !important; text-align: center; color: #1565C0; margin-bottom: 20px; }
    h2, h3 { font-weight: 700 !important; text-align: center; color: #1E88E5; }

    .stTextInput>div>div>input { text-align: right; }

    /* اصلاح فاصله‌ی آیکون و متن در باکس‌های کشویی */
    .stSelectbox>div>div>div { padding-right: 15px; }
    .stMultiSelect>div>div>div { padding-right: 15px; }
    [data-testid="stExpander"] summary { padding-right: 15px; }

    .date-label { font-size: 14px; font-weight: 700; margin-bottom: -15px; color: #424242; }

    /* استایل تایم‌لاین */
    .timeline-container { border-right: 4px solid #1E88E5; padding-right: 20px; margin-right: 15px; margin-top: 10px; }
    .timeline-item { margin-bottom: 25px; padding: 15px; background-color: #f8f9fa; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); position: relative; }
    .timeline-item::before { content: ''; position: absolute; width: 16px; height: 16px; background-color: #1E88E5; border-radius: 50%; right: -30px; top: 15px; }
    .timeline-date { color: #43A047; font-weight: 900; font-size: 1.1em; margin-bottom: 8px; }

    /* استایل باکس‌های خلاصه */
    .summary-card { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 4px solid; height: 100%; }
    .card-title { font-weight: 900; font-size: 1.2em; margin-bottom: 15px; }
    .card-item { margin-bottom: 8px; font-size: 0.95em; }
    </style>
""", unsafe_allow_html=True)

today_jdate = jdatetime.date.today()
today_shamsi = today_jdate.strftime("%Y/%m/%d")
form_data = {}


# --- توابع کمکی ---
def shamsi_date_picker(label_text, key_prefix):
    st.markdown(f"<p class='date-label'>{label_text}</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1.5])
    days = [str(i).zfill(2) for i in range(1, 32)]
    months = ["۰۱ فروردین", "۰۲ اردیبهشت", "۰۳ خرداد", "۰۴ تیر", "۰۵ مرداد", "۰۶ شهریور", "۰۷ مهر", "۰۸ آبان", "۰۹ آذر",
              "۱۰ دی", "۱۱ بهمن", "۱۲ اسفند"]
    years = [str(i) for i in range(1402, 1410)]
    with c1: day = st.selectbox("روز", days, index=today_jdate.day - 1, key=f"{key_prefix}_day")
    with c2: month = st.selectbox("ماه", months, index=today_jdate.month - 1, key=f"{key_prefix}_month")
    with c3: year = st.selectbox("سال", years, index=years.index(str(today_jdate.year)), key=f"{key_prefix}_year")
    return f"{year}/{month.split(' ')[0]}/{day}"


def render_task_group(group_name, sub_tasks, serial_fields=None):
    with st.expander(f"🔽 {group_name}", expanded=False):
        selected = []
        for sub in sub_tasks:
            if st.checkbox(sub, key=f"{group_name}_{sub}"):
                selected.append(sub)

        if selected:
            form_data[group_name] = selected
            if serial_fields:
                st.markdown("---")
                st.caption("⚠️ لطفاً شماره سریال‌های مربوطه را وارد کنید:")
                cols = st.columns(len(serial_fields))
                for idx, field in enumerate(serial_fields):
                    form_data[field] = cols[idx].text_input(field, key=f"serial_{field}")


# --- منوی کناری ---
st.sidebar.title("⚡ سیستم تسلا")
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("منوی اصلی:", ["📝 ثبت اطلاعات تولید", "📊 پنل مدیریت و رهگیری"])
st.sidebar.markdown("---")
st.sidebar.info("نسخه لوکال (آفلاین)")

# =====================================================================
# صفحه اول: ثبت اطلاعات تولید
# =====================================================================
if app_mode == "📝 ثبت اطلاعات تولید":
    st.title("🏭 فرم ثبت لاگ تولید")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        serial_number = st.text_input("شماره سریال دستگاه:", placeholder="مثال: PE2025TS016")
    with col2:
        technicians = st.multiselect("تکنسین(ها) / اپراتورها:",
                                     ["مهدی نجاتیان", "سجاد محبی", "محمدسعید کبیری", "امیرعلی نرجه", "خانم وفایی",
                                      "خانم ستایش", "خانم آشنا", "پرسنل موقت / سایر"],
                                     placeholder="چه کسانی این کار را انجام دادند؟")

    st.markdown("---")

    # حذف اعداد از گزینه‌های لیست کشویی
    department = st.selectbox("بخشی که روی آن کار کرده‌اید را انتخاب کنید:", [
        "📌 یک بخش را انتخاب کنید...", "باکس الکترونیک", "استند", "سیت", "هندل", "کنترل کیفیت (QC)", "تعمیرات",
        "مشخصات مشتری"
    ])

    if department != "📌 یک بخش را انتخاب کنید...":
        st.write(f"**لطفاً ریزفعالیت‌های خود را در بخش '{department}' مشخص کنید:**")

        # حذف اعداد از شرط‌های برنامه
        if department == "باکس الکترونیک":
            render_task_group("بستن بدنه باکس",
                              ["بستن قسمت L شکل", "جایگاه منابع", "جایگاه خازن", "بستن فن ها و گارد", "زدن پرچی بدنه",
                               "نصب قطعات (رله، ترمینال، EMI)"])
            render_task_group("سیم‌کشی",
                              ["سیم کشی منابع و رله", "سیم زدن بخش DC و AC", "سیم زدن بخش قدرت (وارنیش و کابل‌شو)"])
            render_task_group("مونتاژ برد پاور",
                              ["مونتاژ قطعات ریز", "مونتاژ قطعات درشت", "اتصال قطعات قدرت به هیت سینک", "تست جریان کشی",
                               "نصب برد روی بدنه"], ["سریال برد پاور"])
            render_task_group("مونتاژ برد دیجیتال",
                              ["مونتاژ قطعات", "تست ارسال دستور و مشاهده سیگنال ها", "نصب برد روی بدنه"],
                              ["سریال برد دیجیتال"])
            render_task_group("مونتاژ برد رکتیفایر", ["مونتاژ قطعات", "تست مشاهده ولتاژ خروجی", "نصب برد روی بدنه"],
                              ["سریال برد رکتیفایر"])
            render_task_group("مجموعه خازن و هیت سینک",
                              ["شستن هیت سینک ها", "جایگذاری تریستور و دیود", "اتصال به خازن و هارتینگ",
                               "جایگذاری در باکس"], ["سریال تریستور", "سریال دیود", "سریال خازن"])

        elif department == "استند":
            render_task_group("آماده سازی مکانیکی", ["سوراخ کاری بدنه", "نصب تفلون کف", "رنگ آمیزی بدنه"])
            render_task_group("مجموعه نمایشگر (HMI)", ["پروگرام کردن HMI", "مونتاژ قاب HMI", "نصب HMI روی بدنه"])

        elif department == "سیت":
            render_task_group("ساخت کویل سیت",
                              ["برش سیم و لخت کردن", "روکش سیم با وارنیش نسوز", "پیچیدن کویل", "اتصال بخش انتهایی"])
            render_task_group("آماده سازی فن", ["پرچی زدن فن", "سیم زدن فن ها", "جایگذاری فن ها"])
            render_task_group("مونتاژ کویل و فن بر روی سیت", [
                "سوراخ زدن جای فن ها بر روی سیت",
                "نصب فن ها",
                "برش لوله خرطومی",
                "چسباندن فیبر استخوانی و جایگاه بست ها",
                "اتصال کابل ها به هارتینگ",
                "تست تحریک مغناطیسی",
                "تست لقی و گرفتن لقی در صورت وجود"
            ], ["شماره سریال سیت"])

        elif department == "هندل":
            render_task_group("ساخت و مونتاژ هندل",
                              ["ساخت کویل هندل", "سیم‌‌کشی کانکتورهای نظامی", "بستن بدنه اصلی هندل"],
                              ["شماره سریال هندل"])

        elif department == "کنترل کیفیت (QC)":
            qc_type = st.radio("مرحله کنترل کیفیت:", ["حین تولید (In-Process QC)", "نهایی محصول (Final QC)"])
            if qc_type == "حین تولید (In-Process QC)":
                render_task_group("تست‌های میانی (حین تولید)",
                                  ["تست جریان کشی (برد پاور/دیجیتال)", "تست مشاهده سیگنال (برد دیجیتال)",
                                   "تست ولتاژ خروجی (رکتیفایر)", "تست تحریک مغناطیسی", "تست لقی (سیت/هندل)",
                                   "تست عدم برخورد فن"])
                form_data["نتیجه تست حین تولید"] = st.radio("وضعیت قطعه/ماژول:", ["تایید ✔️", "نیاز به اصلاح ⚠️"])
            else:
                form_data["دفعات تست نهایی"] = st.number_input("دفعات تست نهایی (۲۰ دقیقه در فرکانس‌های مختلف):",
                                                               min_value=1, max_value=50, value=1)
                form_data["نبود خط و خش"] = st.checkbox("تایید نبود خط و خش و سلامت ظاهری بدنه")
                form_data["وضعیت نهایی دستگاه"] = st.radio("تصمیم نهایی واحد QC:",
                                                           ["مجوز خروج (Pass) ✅", "بازگشت به خط (Rework) ❌",
                                                            "رد (Fail) 🚫"])

            form_data["توضیحات QC"] = st.text_area("یادداشت بازرس کنترل کیفیت:")
            form_data["نوع QC"] = qc_type

        elif department == "تعمیرات":
            st.write("---")
            form_data["تاریخ اعلام خرابی"] = shamsi_date_picker("تاریخ اعلام خرابی:", "repair_start")
            form_data["علت خرابی"] = st.text_area("علت خرابی (گزارش شده):")
            form_data["شرح تعمیر"] = st.text_area("فعالیت انجام شده برای رفع ایراد:")
            if st.checkbox("آیا قطعه‌ای تعویض شد؟"):
                col_a, col_b = st.columns(2)
                with col_a: form_data["قطعه جایگزین"] = st.text_input("نام قطعه جایگزین:")
                with col_b: form_data["سریال قطعه جدید"] = st.text_input("سریال قطعه جدید:")
            form_data["تاریخ اتمام فعالیت"] = shamsi_date_picker("تاریخ اتمام تعمیر:", "repair_end")

        elif department == "مشخصات مشتری":
            c1, c2 = st.columns(2)
            with c1:
                form_data["نام مشتری"] = st.text_input("نام مشتری/مرکز:")
            with c2:
                form_data["شماره تماس"] = st.text_input("شماره تلفن:")
            form_data["آدرس"] = st.text_area("آدرس مرکز:")
            form_data["وضعیت گارانتی"] = st.selectbox("گارانتی:", ["فعال", "منقضی", "بدون گارانتی"])
            st.write("---")
            form_data["تاریخ خروج"] = shamsi_date_picker("تاریخ تحویل به مشتری:", "delivery")

        st.markdown("---")
        if st.button("💾 ثبت لاگ تولید", use_container_width=True):
            if not serial_number or not technicians:
                st.error("❌ لطفا ابتدا 'شماره سریال دستگاه' و 'نام تکنسین(ها)' را در بالای صفحه وارد کنید.")
            else:
                timestamp_shamsi = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                clean_data = {k: v for k, v in form_data.items() if v}
                tech_names = " و ".join(technicians)
                st.success(f"✅ فعالیت شما با موفقیت برای دستگاه '{serial_number}' توسط تیم [{tech_names}] ثبت شد!")

                with st.expander("مشاهده داده‌های ساختاریافته (جهت ارسال به سرور)"):
                    st.json({
                        "Date (Shamsi)": timestamp_shamsi,
                        "Device_Serial": serial_number,
                        "Technicians": technicians,
                        "Module": department,
                        "Activities": clean_data
                    })

# =====================================================================
# صفحه دوم: پنل مدیریت
# =====================================================================
elif app_mode == "📊 پنل مدیریت و رهگیری":
    st.title("📊 داشبورد وضعیت دستگاه")
    st.markdown("---")

    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
    with search_col1:
        search_query = st.text_input("🔍 جستجوی شماره سریال دستگاه:", placeholder="مثلا PE2025TS016...")
    with search_col2:
        st.write("");
        st.write("")
        search_btn = st.button("جستجوی اطلاعات", use_container_width=True)

    if search_btn and search_query:
        st.success(f"نتایج یافت شده برای دستگاه: **{search_query}**")

        st.markdown("### 📋 خلاصه وضعیت دستگاه")
        st.markdown("""
        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 30px;">
            <div class="summary-card" style="flex: 1; min-width: 250px; border-top-color: #4CAF50;">
                <div class="card-title" style="color: #4CAF50;">🏢 مشتری و گارانتی</div>
                <div class="card-item"><strong>تاریخ تحویل:</strong> ۱۴۰۳/۰۶/۲۵</div>
                <div class="card-item"><strong>وضعیت گارانتی:</strong> فعال 🟢</div>
            </div>
            <div class="summary-card" style="flex: 1; min-width: 250px; border-top-color: #2196F3;">
                <div class="card-title" style="color: #2196F3;">⚙️ سریال ماژول‌ها</div>
                <div class="card-item"><strong>برد پاور:</strong> BP-10023</div>
                <div class="card-item"><strong>برد دیجیتال:</strong> BD-9941</div>
                <div class="card-item"><strong>سریال سیت:</strong> ST-4509</div>
            </div>
            <div class="summary-card" style="flex: 1; min-width: 250px; border-top-color: #FF9800;">
                <div class="card-title" style="color: #FF9800;">🛡️ وضعیت QC</div>
                <div class="card-item"><strong>تست خط و خش:</strong> تایید شده ✔️</div>
                <div class="card-item"><strong>وضعیت نهایی:</strong> <span style="color:green; font-weight:bold;">مجوز خروج ✅</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔍 لاگ کامل خط تولید")
        with st.expander("نمایش ریزِ تاریخچه تولید (تایم‌لاین)"):
            st.markdown(f"""
            <div class="timeline-container">
                <div class="timeline-item">
                    <div class="timeline-date">🟢 ۱۴۰۳/۰۶/۱۵ - ۱۰:۳۰ صبح</div>
                    <div class="timeline-detail"><b>👤 تیم تکنسین:</b> سجاد محبی، مهدی نجاتیان</div>
                    <div class="timeline-detail"><b>🏭 دپارتمان:</b> سیت (مونتاژ کویل و فن بر روی سیت)</div>
                    <div class="timeline-detail" style="color: #555;">
                        <b>فعالیت‌ها:</b> سوراخ زدن جای فن ها بر روی سیت، نصب فن ها، اتصال کابل ها به هارتینگ.<br>
                        <b>سریال ثبت شده:</b> ST-4509
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
