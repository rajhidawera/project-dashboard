import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'الخطة التشغيلية 2025 المعتمدة من الرئيس التنفيذي 20 - 2 -2025.xlsx'
df = pd.read_excel(file_path, sheet_name='لوحة اطلاق المشاريع')

# Cleanup: drop rows where 'المجال' or 'المشاريع' is NaN
df = df.dropna(subset=['المجال', 'المشاريع'])

# Normalize التوقيع column: 1 => 'تم التوقيع', NaN => 'لم يتم التوقيع'
df['حالة التوقيع'] = df['التوقيع'].apply(lambda x: 'تم التوقيع' if x == 1 else 'لم يتم التوقيع')

# Sidebar filter by مجال
selected_fields = st.sidebar.multiselect("اختر المجال", options=df['المجال'].unique(), default=df['المجال'].unique())
df_filtered = df[df['المجال'].isin(selected_fields)]

# Summary statistics
total_projects = df_filtered.shape[0]
signed_projects = df_filtered[df_filtered['حالة التوقيع'] == 'تم التوقيع'].shape[0]
signed_percentage = (signed_projects / total_projects * 100) if total_projects > 0 else 0

# Header
st.title("لوحة حالة المشاريع حسب المجال")

# KPIs
st.metric("إجمالي المشاريع", total_projects)
st.metric("عدد المشاريع الموقعة", signed_projects)
st.metric("نسبة المشاريع الموقعة", f"{signed_percentage:.1f}%")

# Bar chart: عدد المشاريع حسب المجال وحالة التوقيع
grouped = df_filtered.groupby(['المجال', 'حالة التوقيع']).size().reset_index(name='عدد المشاريع')
fig = px.bar(grouped, x='المجال', y='عدد المشاريع', color='حالة التوقيع', barmode='group', title="توزيع المشاريع حسب المجال وحالة التوقيع")
st.plotly_chart(fig)

# Table
st.subheader("تفاصيل المشاريع")
st.dataframe(df_filtered[['المجال', 'المشاريع', 'الجهة المنفذة', 'حالة التوقيع']].reset_index(drop=True))
