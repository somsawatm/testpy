import streamlit as st
import pandas as pd
from datetime import date

# --- 1. Logic Layer ---
def calculate_death_benefit(join_date):
    """คำนวณเงินจัดการศพตามระเบียบข้อ 17.6"""
    days = (date.today() - join_date).days
    years = days / 365

    if days < 180:
        return 0
    elif days < 365:
        return 1500
    elif years < 2:
        return 3000
    elif years < 5:
        return 6000
    elif years < 8:
        return 10000
    elif years < 12:
        return 12000
    elif years < 15:
        return 20000
    else:
        extra_years = int(years - 15)
        return 20000 + (max(0, extra_years) * 500)


def check_membership_status(last_payment_date):
    """เช็คสถานะสมาชิกตามระเบียบข้อ 7.4"""
    days_overdue = (date.today() - last_payment_date).days
    if days_overdue > 90:
        return "พ้นสภาพ (ขาดส่งเกิน 90 วัน)", "error"
    return "ปกติ", "success"


# --- 2. UI Layer ---
st.set_page_config(page_title="Sadao Smart Welfare", layout="wide")

st.title("🏛️ ระบบสวัสดิการชุมชนดิจิทัล เทศบาลเมืองสะเดา")
st.subheader("Sadao City Data Platform - Smart Life Dashboard")

menu = st.sidebar.selectbox(
    "เมนูการใช้งาน",
    ["Dashboard สมาชิก", "ยื่นคำร้องขอเบิก", "ตรวจสอบสถานะสมาชิก (เจ้าหน้าที่)"]
)

# ข้อมูลตัวอย่าง
member_info = {
    "name": "นายสะเดา มีความสุข",
    "join_date": date(2020, 1, 1),
    "last_payment": date(2026, 3, 20),
    "medical_used": 5,
    "total_savings": 2200
}

# ------------------ Dashboard ------------------
if menu == "Dashboard สมาชิก":
    st.header(f"ยินดีต้อนรับ, {member_info['name']}")

    status, status_type = check_membership_status(member_info['last_payment'])
    death_benefit = calculate_death_benefit(member_info['join_date'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("สถานะสมาชิก", status)
        if status_type == "error":
            st.warning("กรุณาติดต่อกองสวัสดิการ")

    with col2:
        st.metric("ยอดเงินออมรวม (บาท)", f"{member_info['total_savings']:,}")

    with col3:
        st.metric("สิทธิเงินจัดการศพ", f"{death_benefit:,} บาท")
        st.caption("ตามระเบียบข้อ 17.6")

    with col4:
        remaining_med = 12 - member_info['medical_used']
        st.metric("สิทธิค่ารักษาคงเหลือ", f"{remaining_med} / 12 คืน")
        st.progress(remaining_med / 12)

    st.divider()
    st.subheader("📈 ประวัติการออมเงิน (วันละ 1 บาท)")

    chart_data = pd.DataFrame({
        'ยอดสะสม': [2100, 2130, 2160, 2190, 2200]
    }, index=['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'ปัจจุบัน'])

    st.line_chart(chart_data)


# ------------------ Form ------------------
elif menu == "ยื่นคำร้องขอเบิก":
    st.header("📝 ยื่นคำร้องขอเบิกสวัสดิการออนไลน์")

    with st.form("welfare_form"):
        welfare_type = st.selectbox("ประเภทสวัสดิการ", [
            "ค่ารักษาพยาบาล (นอนโรงพยาบาล)",
            "สวัสดิการคลอดบุตร",
            "สวัสดิการช่วยเหลือกรณีประสบภัยธรรมชาติ",
            "กรณีเสียชีวิต (สำหรับผู้รับผลประโยชน์)"
        ])

        amount_requested = st.number_input(
            "จำนวนวันที่นอน/วงเงินที่ขอเบิก",
            min_value=1
        )

        doc = st.file_uploader("แนบเอกสารประกอบ", type=["pdf", "jpg", "png"])

        note = st.text_area("รายละเอียดเพิ่มเติม")

        submitted = st.form_submit_button("ส่งคำร้อง")

        if submitted:
            st.success("ส่งคำร้องสำเร็จ! เจ้าหน้าที่จะตรวจสอบภายใน 30 วัน")


# ------------------ Admin ------------------
elif menu == "ตรวจสอบสถานะสมาชิก (เจ้าหน้าที่)":
    st.header("🔍 ระบบสืบค้นข้อมูลสมาชิก (Admin Only)")

    search_id = st.text_input("กรอกเลขบัตรประชาชน หรือเลขสมาชิก")

    if search_id:
        st.success("พบข้อมูลสมาชิก")
        st.write("สถานะ: ปกติ")
        st.write("ประวัติการส่งเงินสมทบครบถ้วน")