#  导入需要用的程序包 
#  import necessary packages
import streamlit as st
import pandas as pd
import json

#  预先定义一些课表相关的元数据 
#  define some meta-data for my timetable
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
periods = ['第1节\n08:00-09:35', '第2节\n09:50-12:15', '第3节\n13:30-15:05', '第4节\n15:20-16:55', '第5节\n17:05-18:40', '第6节\n19:20-21:45']

#  从csv文件中读取课程数据 
#  read courses data from csv file
df = pd.read_csv('data/course_data.csv') # 这里存放了我选的课程
df_timetable = pd.DataFrame(index=periods, columns=days) # 这里初始化一个空的课表，之后把课程填进去
df_owncourse = pd.read_csv('data/own_course.csv') # 这里存放了本院开设的课程

#  数据格式的预处理函数，可以无视
#  a pre-processing function, ignore this
def remove_dollarsigns(x):
    if isinstance(x, str):
        return x.strip("$")
    return x

#  “查看”按钮的响应函数，修改了系统中储存的当前查看的课程序号
#  callback function of "view" button, which changes the system-stored value of course number user is viewing
def call_back_viewCourseDetail(index):
    st.session_state.detail_index = index

#  使用循环，将我选的课程依次放进课表的对应位置
#  using a loop to fill my courses in their proper position of the timetable
for _, course in df.iterrows():
    c_period = course['上课时间'].strip("$")
    c_period = c_period.split("-")
    c_info = f"{course['课程名']}"
    df_timetable.at[periods[int(c_period[1]) - 1], days[int(c_period[0]) - 1]] = c_info

#  预处理读取的数据
#  pre-processing the read data
df_owncourse['课程编号'] = df_owncourse['课程编号'].apply(remove_dollarsigns)
df_owncourse['上课时间'] = df_owncourse['上课时间'].apply(remove_dollarsigns)
df_owncourse['课序号'] = df_owncourse['课序号'].astype(str)
df_owncourse['学分'] = df_owncourse['学分'].astype(str)
df_owncourse['起始周'] = df_owncourse['起始周'].astype(str)
df_owncourse['结束周'] = df_owncourse['结束周'].astype(str)
df_timetable.fillna("", inplace=True) # 把课表空着的位置变成空格，而不是“N/A”
df_owncourse.index += 1 # 院系课程的序号会从1开始而不是0


#  主要负责绘制界面的部分，此后的代码在每次页面有变化时都会重新运行一次，在当时的状态会运行到的语句效果会出现在页面上
#  main function to draw the page, code from here will rerun once something on page is changing, 
#  statements executed will show their content on the page
if __name__ == "__main__":
    
    st.set_page_config(
        page_title="My Tsinghua Homepage", # 页面的名字
        page_icon="", # 页面图标的路径
        layout="wide", # 页面布局方式
    )

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #fff !important;
            }
            body, div, p, span, h1, h2, h3, h4, h5, h6, table, th, td {
                color: #000 !important;
            }
            button, .stButton>button, .stDownloadButton>button {
                background-color: #fff !important;
            }
            div.object-key-val {
                background-color: #fff !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    if "detail_index" not in st.session_state:
        st.session_state.detail_index = 0 # 初始化当前查看的课程序号为0，此时未查看任何一门课程的信息

    st.markdown('<h1 style="color: #5c307d; text-align:center;">自我介绍</h1>', unsafe_allow_html=True) # 大标题

    tab_info, tab_timetable, tab_owncourse = st.tabs(["个人主页", "整体课表", "课程资源"])

    # 个人信息栏，分了两列把内容堆上去
    # personal info tab, pile all lines in 2 colomns
    with tab_info:
        st.subheader("个人信息")
        col1, col2 = st.columns([2,5]) # col1是头像，col2是其他信息
        col1.image("data/1.jpg", width=200)
        with col2.container(): # 里面又分了两列
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**姓名**：许瀚元")
            col2_2.markdown("**年龄**：18")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**性别**：男")
            col2_2.markdown("**家乡**：江苏省淮安市")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**学校**：清华大学")
            col2_2.markdown("**专业**：笃实书院")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**爱好**：编程 打篮球 拉小提琴")
            col2_2.markdown("**生日**：20070704")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**Tel**：18800660556")
            col2_2.markdown("**E-Mail**：xhy25@mails.tsinghua.edu.cn")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**地址**：北京市海淀区清华大学紫荆公寓7号楼")
            col2_2.markdown("**我的github**： [fallingstar56](https://github.com/fallingstar56)")

        st.markdown(
            """
            <div style="
            margin-top:40px;
            margin-bottom:0px;
            padding:20px;
            background-color:#f5f3fa;
            border-radius:20px;
            box-shadow:0 2px 8px rgba(92,48,125,0.08);
            text-align:center;
            font-size:18px;
            color:#000;
            ">
            大家好，我叫许瀚元，欢迎访问我的个人页面。我是清华大学笃实书院的五字班学生，<br>
            我对软件工程有浓厚的兴趣，我学习过包括C、C++、Java、Python等多种编程语言以及一些信息领域前沿技术。<br>
            目前我选修了刘璘老师开设的创意软件课程，期待与大家在课堂上交流，共同度过一段开心的时光。
        </div>
        """,
        unsafe_allow_html=True
        )
        
    center_col = st.columns([2, 1, 2])[1]
    with center_col:
        st.image("data/thu.jpg", width=150)

    # 学期课表栏，这里把之前填好的课表展示了一下
    # timetable tab, show the filled timetable
    with tab_timetable:
        st.subheader("学期课表")
        st.dataframe(df_timetable, use_container_width=True) # 这样就可以展示一个dataframe

        csv_download = df_timetable.to_csv().encode('utf-8')
        st.download_button(
            label="获取我的课表",
            data=csv_download,
            file_name='timetable_Ruanxx.csv',
            mime='text/csv',
        ) # 下载按钮

    # 本院开课栏，这里把读取的本院课程展示了一下
    # own course tab, show all courses of THSS
    with tab_owncourse:
        st.subheader("本院开课")
        st.dataframe(df_owncourse[['课程名', '课程编号', '课序号', '学分', '任课教师', '上课时间']], use_container_width=True, height=400) # 这样就可以展示一个dataframe
        index_input = st.number_input(min_value=1,max_value=len(df_owncourse),label="查找详情",placeholder="输入序号") # 这是一个输入框
        st.button("查看", on_click=lambda: call_back_viewCourseDetail(index_input)) # 查看按钮，会将输入框的数值设置到系统里

        if st.session_state.detail_index != 0: # 如果系统里当前存储了要查看的数值，展示对应的详细信息
            course = df_owncourse.iloc[st.session_state.detail_index - 1] # 从dataframe中取出选中的课程
            course_dict = course.to_dict() # 转成dict形式
            course_json = json.dumps(course_dict, ensure_ascii=False) # 再转成json形式
            st.json(course_json, expanded=2) # 这样就可以展示一个json