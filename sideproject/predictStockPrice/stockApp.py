#---------Imports
from tkcalendar import Calendar, DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
# try:
#     from tkinter import *
#     import tkinter as tk
#     from tkinter import ttk
# except ImportError:
#     import Tkinter as tk
#     import ttk
# from tkinter import Frame,Label,Entry,Button, LabelFrame, Listbox, Scrollbar
from tkinter import *
import tkinter as tk
from tkinter import ttk

import pandas_datareader as pdr
import pandas as pd 
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib import style

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import csv
#---------End of imports

class CusCalendar():
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=2018, month=2, day=5)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, width="14", text="선택", command=self.select_date).pack(side="left", padx=5, pady=5)
        ttk.Button(self.top, width="14", text="창닫기", command=self.destory_win).pack(side="left", padx=5, pady=5)
        # self.date = ''
        # self.top.grab_set()

    def select_date(self):
        self.date = self.cal.selection_get()
        self.top.destroy()

    def destory_win(self):
        self.date = ''
        self.top.destroy()
    pass


class Stock():
   
    def __init__(self):
        self.stockType = {'kospi': 'stockMkt', 'kosdaq':'kosdaqMkt'}
        pass

    # 주식종목타입가져오기
    def getStockCode(df, name):
        code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
        code = code.strip()
        return code  

    # 주식종목타입별 데이터 다운로드
    def getDownloadStockData(self, marketTypeParam=None):
        marketType = self.stockType[marketTypeParam]
        downloadLink = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        downloadLink = downloadLink + '&marketType=' + marketType  
        # print(downloadLink)
        df = pd.read_html(downloadLink, header=0)[0]
        return df

    #코스피 데이터 다운로드
    def getDownloadKospi(self):
        df = self.getDownloadStockData('kospi')
        # print("KOSPI INDEX :" + df)
        df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
        return df

    #코스닥 데이터 다운로드
    def getDownloadKosdaq(self):
        df = self.getDownloadStockData('kosdaq')
        df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
        return df

    def saveStockCodeToCsv(self, BASE_DIR):
        # 주식 종목 및 회사 데이터 가지고와서 회사명, 종목코드 합쳐서 csv 데이터로 저장 하기 
        kospidf = self.getDownloadKospi()
        kospidf.to_csv(BASE_DIR + '/KOSPI.csv', sep=',', na_rep='NaN')

        kosdaqdf = self.getDownloadKosdaq()
        kosdaqdf.to_csv(BASE_DIR + '/KOSDAQ.csv', sep=',', na_rep='NaN')
        # codedf = pd.concat([kospidf,kosdaqdf])
        # codedf = codedf[['회사명','종목코드']]
        # codedf = codedf.rename(columns={'회사명':'name', '종목코드':'code'})
        # codedf.to_csv(BASE_DIR + '/stockcode.csv', sep=',', na_rep='NaN')

    def getStockDataByStockCode():
        code = self.getStockCode(codedf, '카카오')
        df = pdr.get_data_yahoo(code, adjust_price=True)

    pass


class App(Frame):
    def __init__(self, BASE_DIR,  master = None):
        Frame.__init__(self, master)
        self.master = master
        self.BASE_DIR = BASE_DIR
        self.init_window()  

        self.style = ttk.Style()
        self.style.configure("customstyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        self.style.configure("customstyle.Treeview.Heading",highlightthickness=0, bd=0, font=('Calibri', 12,'bold')) # Modify the font of the headings
        self.style.layout("customstyle.Treeview", [('customstyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        import datetime
        self.today = datetime.date.today()
        # print(today)

        self.simmul_startdate.delete(0, END) 
        self.simmul_startdate.insert(0, '{}'.format(self.today))

        self.simmul_enddate.delete(0, END)
        self.simmul_enddate.insert(0, '{}'.format(self.today))
    
        self.start_date = ''
        self.end_date   = ''
        self.master.bind("<Return>", self.startSimmulation)
        pass

    def init_window(self):
        self.master.title("Monte Carlo Simmulations")

        self.left_frame = Frame(self.master, padx=5, pady=5, relief='sunken', bd=0)
        self.left_frame.grid(row=0, column=0, sticky='new')
 
        #주식 종목 파일 버튼 프레임
        self.stock_btn_frame = Frame(self.left_frame, padx=5, pady=5, relief='sunken', bd=0)
        self.stock_btn_frame.grid(row=0, column=0, sticky='new')

        self.btn_add_file = Button(self.stock_btn_frame, padx=5, pady=5, width=12,  text="KOSPI", command=self.ReadStockDataToViewTreeView)
        self.btn_add_file.pack(side="left", padx=5, pady=5)

        self.btn_del_file = Button(self.stock_btn_frame, padx=5, pady=5, width=12, text="KOSDAQ")
        self.btn_del_file.pack(side="left", padx=5, pady=5)

        self.btn_update_file = Button(self.stock_btn_frame,  pady=5, width=12, text="종목업데이트", command=self.UpdateStockCode)
        self.btn_update_file.pack(side="right", pady=5)

        #주식 정보 리스트 프레임
        self.list_frame = Frame(self.left_frame, relief='sunken', bd=1)
        self.list_frame.grid(row=1, column=0, sticky='new', padx=5, pady=5,  )

        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill='y')

        # self.list_file = Listbox(self.list_frame, selectmode="extended",height=5, bd=0, relief=SUNKEN,  yscrollcommand=self.scrollbar.set)
        # self.list_file.pack(side='left',ipadx=5, padx=5, pady=5,  fill='both', expand=True)
        # self.tree_view = Treeview(self.list_frame,  bd=0, relief=SUNKEN,  yscrollcommand=self.scrollbar.set)

        self.tree_view = ttk.Treeview(self.list_frame, style="customstyle.Treeview", height=5, yscrollcommand=self.scrollbar.set)
        self.tree_view.tag_configure('odd', background='#E8E8E8')
        self.tree_view.tag_configure('even', background='#ffffff')
        self.tree_view["columns"]=("id","name","code")

        self.tree_view.column("#0", width=0,stretch=NO)
        self.tree_view.column("id", width=50, anchor=CENTER )
        self.tree_view.column("name", width=230, anchor=CENTER )
        self.tree_view.column("code", width=230, anchor=CENTER)

        self.tree_view.heading("#0", text="" )
        self.tree_view.heading("id", text="ID", anchor=W)
        self.tree_view.heading("name", text="회사명")
        self.tree_view.heading("code", text="종목코드")

        # self.tree_view.insert(parent='', index='end',  iid=0, text="", values=("1","삼성전자","004594"))
        # self.tree_view.insert(parent='', index='end',  iid=1, text="", values=("2","삼성전자","004594"))
        # self.tree_view.insert(parent='', index='end',  iid=3, text="", values=("3","한국전자","004594"))
        # self.tree_view.insert(parent='', index='end',  iid=4, text="", values=("4","엘지전자","004594"))
        # self.tree_view.insert(parent='', index='end',  iid=5, text="", values=("5","현대자동차","004594"))
        # self.tree_view.insert(parent='', index='end',  iid=6, text="", values=("6","sk반도체","004594"))
        # self.tree_view.insert(parent=" ", index='end',  text="Line 1", values=("1A","1b"))
        # self.tree_view.insert(parent=" ", index='end',  text="Line 1", values=("1B","1b"))

        # id2 = self.tree_view.insert("", 1, "dir2", text="Dir 2")
        # self.tree_view.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))


        # ##alternatively:
        # self.tree_view.insert("", 3, "dir3", text="Dir 3")
        # self.tree_view.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

        self.tree_view.pack(side='left', fill='both', expand=True)

        self.scrollbar.config(command=self.tree_view.yview)

        # 실행 날짜 선택, 기간 선택  
        # global simmul_startdate, simmul_enddate
        self.simmuloption_frame = LabelFrame(self.left_frame, text="실행 기간 선택", relief=SOLID, bd=1)
        self.simmuloption_frame.grid(row=2, column=0, sticky='new', padx=5, pady=5)

        self.lbl_simmul_start = Label(self.simmuloption_frame, text="시작일", width=4)
        self.lbl_simmul_start.pack(side="left" , padx=5, pady=5)
        self.simmul_startdate = Entry(self.simmuloption_frame, width=12)
        self.simmul_startdate.pack(side="left", fill='x', ipady=3, padx=5, pady=5)

        self.st_calendar_icon = PhotoImage(file=self.BASE_DIR + "/img/icon/calendar_date.png")
        self.btn_start_calendar = Button(self.simmuloption_frame, bd=0, borderwidth=4, command=self.startPopUPcal) 
        self.btn_start_calendar.config(image=self.st_calendar_icon, width="30", height="30", activebackground="black")
        self.btn_start_calendar.pack(side="left", padx=5, pady=5)        

        self.lbl_simmul_end = Label(self.simmuloption_frame, text="종료일", width=4)
        self.lbl_simmul_end.pack(side="left" , padx=5, pady=5)
        self.simmul_enddate = Entry(self.simmuloption_frame, width=12)
        self.simmul_enddate.pack(side="left", fill='x', ipady=3, padx=5, pady=5)

        self.end_calendar_icon = PhotoImage(file=self.BASE_DIR + "/img/icon/calendar_date.png")
        self.btn_end_calendar = Button(self.simmuloption_frame, bd=0, borderwidth=4, command=self.endPopUpcal) 
        self.btn_end_calendar.config(image=self.end_calendar_icon, width="30", height="30", activebackground="black")
        self.btn_end_calendar.pack(side="left", padx=5, pady=5)


        #시뮬레이션 옵션
        self.option_frame = LabelFrame(self.left_frame, text="시뮬레이션 옵션", relief='solid', bd=1)
        self.option_frame.grid(row=3,column=0, sticky='nwe', padx=5, pady=5)

        self.labelSpeed = Label(self.option_frame,text="Speed (km/Hr)",bd=1, width=12)
        self.labelSpeed.pack(side="left", padx=5, pady=5)
        self.textSpeed = Entry(self.option_frame,width=12)
        self.textSpeed.pack(side="left", padx=5, pady=5)

        self.labelAmplitude = Label(self.option_frame,text="Amplitude",width=12)
        self.labelAmplitude.pack(side="left", padx=5, pady=5)        
        self.textAmplitude = Entry(self.option_frame,width=12)
        self.textAmplitude.pack(side="left", padx=5, pady=5)

        # 진폭 amplitude
        self.textAmplitude.insert(0, "0.5")
        self.A = 0.5
        # 속도 velocity 
        self.textSpeed.insert(0, "2.0") 
        self.v = 2.0

        # 실행버튼 프레임
        self.btn_frame = LabelFrame(self.left_frame, text="실행 버튼 프레임", relief='solid', bd=1)
        self.btn_frame.grid(row=4,column=0, sticky='nwe', padx=5, pady=5)

        # self.buttonPlot = Button(self.btn_frame,text="Plot",command=self.drawPlot,width=12, padx=5, pady=5)        
        # self.buttonPlot.pack(side="right", padx=5, pady=5)
        self.buttonClear = Button(self.btn_frame,text="옵션리셋",command=self.Clear,width=12, padx=5, pady=5)
        self.buttonClear.pack(side="right", padx=5, pady=5)
        self.buttonClear.bind(lambda e:self.Clear)

        # self.btn_chart = Button(self.btn_frame, padx=5, pady=5, width=12, text="chartDraw")
        # self.btn_chart.pack(side="right", padx=5, pady=5)

        self.btn_cancel_file = Button(self.btn_frame, padx=5, pady=5, width=12, text="취소", command=self.master.quit)
        self.btn_cancel_file.pack(side="right", padx=5, pady=5)
        self.btn_start_file = Button(self.btn_frame, padx=5, pady=5, width=12,  text="예측 시작", command=self.startSimmulation)
        self.btn_start_file.pack(side="right", padx=5, pady=5)

        # 진행 상황 Progress Bar
        self.frame_progress = LabelFrame(self.left_frame, text="진행 상황", relief=SOLID, bd=1, height=20)
        self.frame_progress.grid(row=5, column=0, sticky='nwe', padx=5, pady=5)

        self.p_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame_progress, maximum=100, variable=self.p_var)
        self.progress_bar.pack(fill='x', padx=5, pady=5)
        self.progress_bar.start(50)

    # 종목 업데이트
    def UpdateStockCode(self):
        print("종목코드 업데이트 start")
        _stock = Stock()
        _stock.saveStockCodeToCsv(self.BASE_DIR)
        print("종목코드 업데이트 ")

    # KOSPI 종목 가져와서 Treeview에 넣기 
    def ReadStockDataToViewTreeView(self):
        
        with open(self.BASE_DIR+'/KOSPI.csv','r') as f:
            reader = csv.reader(f)
            count = 0
            for record in reader:
                if count == 0:
                    pass
                else:
                    # print(record[])
                    self.tree_view.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1],record[2]))
                count += 1
        self.clearTreeView()
        # dat = pd.read_csv(self.BASE_DIR+'/KOSPI.csv', encoding = 'utf-8') 
        # print(dat.head())
        # print(dat.describe(include="all"))

        # data = [
        #     ["1", "jhon", "aaaaa"],
        #     ["2", "jhon", "aaaaa"],
        #     ["3", "jhon", "aaaaa"],
        #     ["4", "jhon", "aaaaa"],
        #     ["5", "jhon", "aaaaa"],
        # ]
        # #  self.tree_view.insert(parent='', index='end',  iid=0, text="", values=("1","삼성전자","004594"))
        # count = 0 
        # for record in data:
        #     count += 1
        #     self.tree_view.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1],record[2]))
        # pass

    # Treeview 삭제 
    def clearTreeView(self):
        self.tree_view.delete(*tree_view.get_children())
        

    def startSimmulation(self,event=None):
        #각 옵션들을 확인해서 가져온다. 
        print("시작일", self.simmul_startdate.get())
        print("종료일", self.simmul_enddate.get())
        self.drawPlot()
        

    def drawPlot(self):
        self.v = float(self.textSpeed.get())
        self.A = float(self.textAmplitude.get())

    def animate(self,i):
        # self.line.set_ydata(np.sin(x+i/10.0)) 
        self.line.set_ydata(self.A*np.sin(self.x+self.v*i/10.0))  # update the data
        return self.line,

    def drawGraph(self):
        self.graph_frame = LabelFrame(self.master, text="결과 그래프", relief='solid', bd=1)
        self.graph_frame.grid(row=0,column=1, padx=5, pady=5)
        self.x = 5*np.arange(0, 2*np.pi, 0.01) # x-array
        # self.y = self.amplitude * np.sin(self.frequency * x + self.phase_shift) + self.vertical_shift
        # self.y = np.sin(self.x)
        self.y = self.A * np.sin(self.v * self.x)
        self.fig = plt.Figure(figsize=(5,4), dpi=100)

        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.x, self.y)        
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().grid(column=0,row=0)
        self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, 200), interval=25, blit=False)

        plt.grid()
        # self.ax = plt.axes()
        # self.ax.set_xlim([0, 6.3])
        # self.ax.set_ylim([-3, 3])

    def Clear(self):      
        self.textAmplitude.delete(0, "end")
        self.textAmplitude.insert(0, "0.5")
        self.textSpeed.delete(0, "end")       
        self.textSpeed.insert(0, "2.0")
        self.drawPlot()    

    def startPopUPcal(self):
        _cal = CusCalendar(self.master)
        self.master.wait_window(_cal.top)
        if not _cal.date :
            return 
        else:
            self.start_date = _cal.date
        self.simmul_startdate.delete(0, END) 
        # print("start 선택 날짜 : {}".format(self.start_date) )
        self.simmul_startdate.insert(0, '{}'.format(self.start_date))

    def endPopUpcal(self):
        _cal = CusCalendar(self.master)
        self.master.wait_window(_cal.top)
        # print(type(_cal.date))
        if not _cal.date:
            # print('비어있음')
            return 
        else:
            # print('비어있지 않음')
            self.end_date = _cal.date
        # print('End date: {}'.format(self.end_date))
        self.simmul_enddate.delete(0, END)
        # print("end 선택 날짜 : " + str(cal.selection_get()))
        self.simmul_enddate.insert(0, '{}'.format(self.end_date))
        # self.simmul_enddate.insert(0, cal.selection_get().strftime('%Y-%m-%d'))

def main():
    global BASE_DIR 
    root = Tk()
    root.geometry("1045x440")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    root. resizable(False, False)
    app = App(BASE_DIR, root)

    # print(app.BASE_DIR)
    app.drawGraph()
    root.mainloop()


if __name__ == '__main__':
    main()
    pass

