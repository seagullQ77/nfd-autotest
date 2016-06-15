# -*- coding: utf-8 -*-
from Tkinter import *

import standardGeneratorApi
from loanGeneratorTool import cropGeneratorApi


def loanGui():
    top = Tk()
    top.title('贷款生成器V1.0 by 质量管理部')
    env = IntVar()
    top.geometry('650x600')

    l1=Label(top,text='运行环境选择:')
    l1.grid(row = 0,column =0,sticky=W)
    R1 = Radiobutton(top, text="测试", variable=env, value=1)
    R1.grid(row = 0,column = 1)
    R2 = Radiobutton(top, text="联调", variable=env, value=2)
    R2.grid(row = 0,column = 2)
    R3 = Radiobutton(top, text="体验", variable=env, value=3)
    R3.grid(row = 0,column =3)
    R4 = Radiobutton(top, text="预发布", variable=env, value=4)
    R4.grid(row = 0,column =4)

    lSpace=Label(top,text='-------------普通贷生成区，下面各项必填，约3~5秒生成一条-------------',fg='blue')
    lSpace.grid(row=1,column=0,columnspan=8,sticky=W)

    l2 = Label(top, text='普通贷借款主体：')
    l2.grid(row=2,column=0,sticky=W)
    loanType=IntVar()
    R5 = Radiobutton(top, text="个人", variable=loanType, value=1)
    R5.grid(row=2,column =1)
    R6 = Radiobutton(top, text="企业", variable=loanType, value=2)
    R6.grid(row=2,column =2)

    l3 = Label(top, text='贷款条数：')
    l3.grid(row=3,column=0,sticky=W)

    e1=Entry(top)
    e1.grid(row=3,column=1,columnspan=2)
    def btnStand():#产生普通贷的按钮
        envT = env.get()
        loanT = loanType.get()
        a=e1.get()

        for i in range(int(a)):
            oT= standardGeneratorApi.loanGenerate(envT, loanT)
            Label(top, text=oT,borderwidth=1,fg='red').grid(row=i+7, column=0,columnspan=8)#在底部打印输出生成结果

    b1=Button(top,text='确定生成',command=btnStand)
    b1.grid(row=3,column=3)

    lspace=Label(top,text="----------------富农贷生成区，下面各项必填，约3~5秒生成一条-------------",fg='blue')
    lspace.grid(row=4,column=0,columnspan=8,sticky=W)
    l4 = Label(top, text='富农贷担保方ID：')
    l4.grid(row=5,column=0,sticky=W)
    e2=Entry(top)
    e2.grid(row=5,column=1,columnspan=2)
    l5 = Label(top, text='贷款条数：')
    l5.grid(row=6,column=0,sticky=W)
    e3=Entry(top)
    e3.grid(row=6,column=1,columnspan=2)
    def btnCrop():#产生富农贷的按钮
        envT = env.get()
        g=int(e2.get())
        b=e3.get()
        for i in range(int(b)):
            oT= cropGeneratorApi.loanGenerate(g, envT)
            Label(top, text=oT, borderwidth=1,fg='red').grid(row=i + 7, column=0, columnspan=8)  # 在底部打印输出生成结果

    b2 = Button(top, text='确定生成', command=btnCrop)
    b2.grid(row=6, column=3)

    top.mainloop()
if __name__ == "__main__":
    loanGui()
