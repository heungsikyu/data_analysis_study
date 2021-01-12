from tkcalendar import Calendar, DateEntry
from ttkthemes import ThemedTk
try:
    from tkinter import *
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

from simmulation import Simmulation as simmulate
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk) 
import numpy as np
import random

# window = ThemedTk(theme="arc")
# ttk.Button(window, text="Quit", command=window.destroy).pack()
# window.mainloop()


# root = Tk()
root = ThemedTk(theme="black")
# root.config(background="white")
root.title('Monte Carlo Simmulations')


# initchart = simmulate(root)

# s = ttk.Style()
# s.theme_names()
# s.theme_use('clam')
# # s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')


def calendar():
    def insert_startdate():
        simmul_startdate.delete(0, END)
        simmul_startdate.insert(0, cal.selection_get().strftime('%Y-%m-%d'))

    def insert_enddate():
        simmul_enddate.delete(0, END)
        simmul_enddate.insert(0, cal.selection_get().strftime('%Y-%m-%d'))

    top = tk.Toplevel(root)

    import datetime
    today = datetime.date.today()
    print(today)

    mindate = datetime.date(year=2000, month=1, day=1)
    maxdate = today + datetime.timedelta(days=30)
    # print(mindate, maxdate)

    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                mindate=mindate, maxdate=maxdate, disabledforeground='red',
                cursor="hand1", year=2000, month=1, day=1)
    cal.pack(fill="both", expand=True)
    cal_btn_frame = Frame(top, relief=SUNKEN, bd=0)
    cal_btn_frame.pack(ipady=5)
    ttk.Button(cal_btn_frame, text="start", command=insert_startdate).pack(side='left')
    ttk.Button(cal_btn_frame, text="end", command=insert_enddate).pack(sid='left')


def startSimmulation():
    #각 옵션들을 확인해서 가져온다. 
    print("시작일", simmul_startdate.get())
    print("종료일", simmul_enddate.get())


def graph():
    house_price = np.random.normal(30000, 25000, 5)
    print(house_price)

    data1 = {'Country': ['US','CA','GER','UK','FR'],
         'GDP_Per_Capita': house_price
        }
    df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])

    figure = plt.figure(figsize = (5,4), dpi = 100)
    ax1 = figure.add_subplot(111)
    # house_price.plot(kind='bar', lengend=True, ax=ax1)
    bar1 = FigureCanvasTkAgg(figure, root)
    bar1.get_tk_widget().grid(row=0, column=1)
    df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Country Vs. GDP Per Capita')

    # chart = FigureCanvasTkAgg(figure, root)
    # chart.get_tk_widget().grid(row=0, column=1, rowspan=2)
    # plt.grid()
    # axes = plt.axes()
    # axes.set_xlim([0, 100000])
    # axes.set_ylim([0, 100000])

# figure1 = plt.Figure(figsize=(6,5), dpi=100)
# ax1 = figure1.add_subplot(111)
# bar1 = FigureCanvasTkAgg(figure1, root)
# bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
# df1.plot(kind='bar', legend=True, ax=ax1)
# ax1.set_title('Country Vs. GDP Per Capita')




left_frame = Frame(root, padx=5, pady=5, relief=SUNKEN, bd=0)
left_frame.grid(row=0, column=0, sticky='nsew')

# right_frame = Frame(root, padx=5, pady=5, relief=SUNKEN, bd=1, width=500)
# right_frame.pack(side="right", fill="both", ipadx=5)


#주식 종목 파일 프레임
file_frame = Frame(left_frame, relief=SUNKEN, bd=0)
file_frame.pack(fill="x", ipady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12,  text="KOSPI")
btn_add_file.pack(side="left", padx=5, pady=5)

btn_del_file = Button(file_frame,  padx=5, pady=5, width=12, text="KOSDAQ")
btn_del_file.pack(side="left", padx=5, pady=5)

btn_update_file = Button(file_frame,  pady=5, width=12, text="종목업데이트")
btn_update_file.pack(side="right", pady=5)


#리스트 프레임
list_frame = Frame(left_frame, relief=SUNKEN, bd=0)
list_frame.pack(fill="x", padx=5, pady=5, ipady=5 )

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill='y')
list_file = Listbox(list_frame, selectmode="extended",height=5, bd=1, relief=SUNKEN,yscrollcommand=scrollbar.set)
list_file.pack(side='left',ipadx=5,  fill='both', expand=True)
scrollbar.config(command=list_file.yview)

for item in range(1, 50):
    list_file.insert("end"," "+str(item))

# 진행 상황 Progress Bar
frame_progress = LabelFrame(left_frame, text="진행상황", relief=SOLID, bd=1, height=20)
frame_progress.pack(fill='x', padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill='x', padx=5, pady=5)
progress_bar.start(50)

# simmulation option 
simmuloption_frame = LabelFrame(left_frame, text="Simmulation Option", relief=SOLID, bd=1)
simmuloption_frame.pack(fill="x", padx=5, pady=5, ipady=5)

lbl_simmul_start = Label(simmuloption_frame, text="시작일", width=4)
lbl_simmul_start.pack(side="left" , padx=5, pady=5)
simmul_startdate = Entry(simmuloption_frame, width=12)
simmul_startdate.pack(side="left", fill='x', ipady=3, padx=5, pady=5)

lbl_simmul_end = Label(simmuloption_frame, text="종료일", width=4)
lbl_simmul_end.pack(side="left" , padx=5, pady=5)
simmul_enddate = Entry(simmuloption_frame, width=12)
simmul_enddate.pack(side="left", fill='x', ipady=3, padx=5, pady=5)

calendar_icon = PhotoImage(file="./sideproject/predictStockPrice/img/icon/calendar_date.png")
show_calendar = Button(simmuloption_frame, bd=0, borderwidth=4, command = calendar) 
show_calendar.config(image=calendar_icon, width="30", height="30", activebackground="black")
show_calendar.pack(side="left", padx=5, pady=5)


# 시뮬레이션옵션
lbl_simmul_frame = LabelFrame(left_frame, text="시뮬레이션 옵션", padx=5, pady=5, relief=SOLID, bd=1)
lbl_simmul_frame.pack()

opt_frame = Frame(lbl_simmul_frame)
opt_frame.pack(side="left", padx=5, pady=5)

# Amplitude
lb_Amplitude = Label(opt_frame, text = "Amplitude", width=10)
lb_Amplitude.pack(side='left', padx=5, pady=5)
amplitude_entry = Entry(opt_frame, width = 5)
amplitude_entry.pack(side='left', padx=5, pady=5)

# Frequency
lb_Frequency = Label(opt_frame, text = "Frequency", width=10)
lb_Frequency.pack(side="left", padx=5, pady=5)
frequency_entry = Entry(opt_frame, width = 5)
frequency_entry.pack(side="left", padx=5, pady=5)

# Vertical Shift
lb_vertical_shfit = Label(opt_frame, text = "Vertical Shift")
lb_vertical_shfit.pack(side="left", padx=5, pady=5)
vertical_shift_entry = Entry(opt_frame, width = 5)
vertical_shift_entry.pack(side="left", padx=5, pady=5)

# Horizontal Shift
lb_horizontal_shift = Label(opt_frame, text = "Phase Shift")
lb_horizontal_shift.pack(side="left", padx=5, pady=5)
phase_shift_entry = Entry(opt_frame, width = 5)
phase_shift_entry.pack(side="left", padx=5, pady=5)


btn_frame = Frame(lbl_simmul_frame, bd=1)
btn_frame.pack()
button = Button (btn_frame, text="DrawChart", padx=5, pady=5, width=12, command=graph)
button.pack(side="left", padx=5, pady=5)


# start btn frame
btn_frame = Frame(left_frame, relief=SUNKEN, bd=0)
btn_frame.pack(ipady=5)

btn_chart = Button(btn_frame, padx=5, pady=5, width=12, text="chartDraw", command=graph)
btn_chart.pack(side="right", padx=5)

btn_cancel_file = Button(btn_frame, padx=5, pady=5, width=12, text="취소", command=root.quit)
btn_cancel_file.pack(side="right", padx=5)
btn_start_file = Button(btn_frame, padx=5, pady=5, width=12,  text="예측 시작", command=startSimmulation)
btn_start_file.pack(side="right", padx=5)




# #저장 경로 
# path_frame = LabelFrame(left_frame, text="저장하기", relief=SOLID, bd=1)
# path_frame.pack(fill="x", padx=5, pady=5)

# doc_dest_path = Entry(path_frame)
# doc_dest_path.pack(side="left", fill='x', expand=True, ipady=3, padx=5, pady=5)

# btn_dest_path = Button(path_frame, text='찾아보기',padx=5, pady=5, width=12)
# btn_dest_path.pack(side="right", padx=5, pady=5)


# #옵션 프레임
# frame_option = LabelFrame(left_frame, text="옵션", relief=SOLID, bd=1)
# frame_option.pack(fill="x", padx=5, pady=10)

# #1. 가로 넓이 옵션
# #가로 넓이 레이블
# lbl_width = Label(frame_option, text="가로넓이", width=4)
# lbl_width.pack(side="left" , padx=5, pady=5)

# #가로 넓이 콤보
# opt_width = ["원본 유지", "1024", "800", "640"]
# cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10, height=30)
# cmb_width.current(0)
# cmb_width.pack(side="left", padx=5, pady=5)

# #2. 간격 옵션 
# # 간격 옵션 레이블 
# lbl_space = Label(frame_option, text="간  격", width=4)
# lbl_space.pack(side="left", padx=5, pady=5)

# # 간격 옵션 콤보
# opt_space = ["없음", "좁게", "보통", "넓게"]
# cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
# cmb_space.current(0)
# cmb_space.pack(side="left",padx=5, pady=5)

# #3. 파일 포맷 옵션 
# # 파일 포맷 옵션 레이블 
# lbl_format = Label(frame_option, text="포 맷", width=4)
# lbl_format.pack(side="left", padx=5, pady=10)

# # 파일 포맷 옵션 콤보
# opt_format = ["PNG", "JPG", "BMP"]
# cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
# cmb_format.current(0)
# cmb_format.pack(side="left", padx=5, pady=5)
graph()
root. resizable(False, False)
root.mainloop()

