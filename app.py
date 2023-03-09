#!/usr/bin/env python3.6
# -*- coding:utf-8 -*- 
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

from pyecharts import options as opts
from pyecharts.charts import Bar,Pie,Line
import time,datetime,sys,os
import pandas as pd

#CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates/pyecharts"))
global color_mtk,color_skw,color_google,color_critical,color_normal
color_mtk = '#FF9900'
color_skw = '#0066FF'
color_google = '#009933'
color_blocker = '#990000'
color_critical = '#FF0000'
color_normal = '#00CCFF'
color_open = '#990000'
color_reopened = '#FF6600'
color_inprogress = '#FF9900'
color_resolved = '#66FF00'
color_closed = '#00CC00'

global template_folder
if hasattr(sys,'_MEIPASS'):
    app_path = os.path.join(sys._MEIPASS)
    template_folder = os.path.join(app_path,'templates')
    
app = Flask(__name__,static_folder="static",template_folder='templates')

@app.route("/")#使用Flask的 app.route 装饰器将URL路由映射到该函数
def home(title=None): #自定义传递参数title，在index.html用{{ title }}可以引用改参数
    project = df_cr['Project'].mode()[0] #使用“mode”获得dataframe中每个列的最频繁值
    model = df_cr['Project Model'].mode()[0]
    return render_template("index.html",title=f"MTK eService Issue Statistics-[{project}_{model}]")


'''
    MTK eService 问题统计
'''

@app.route("/allCRIssuesStatus")
def all_CR_Issues_Status():
    print('allCRIssuesStatus')
    b = pie_all_cr_issues_status()
    return b.dump_options_with_quotes()

def pie_all_cr_issues_status() -> Pie:
    #status = ['Submitted', 'Assigned', 'Working','Reworking','Assigned','Resolved'] 
    #counts = [50,40,10,30,60,20]
    #datas = [(o,c) for o,c in zip(status, counts)]
    #[('Submitted', 50), ('Assigned', 40), ('Working', 10), ('Reworking', 30), ('Assigned', 60), ('Resolved', 20)]
    print('df_cr_state:',df_cr_state)
    series_datas = df_cr_state.value_counts()
    print('series_datas state:',series_datas)

    order = ['Submitted', 'Assigned', 'Working','Reworking','Resolved']
    df_reindex = pd.DataFrame(series_datas).loc[order]#按order重新排序
    #print('df_reindex:',type(df_reindex),df_reindex.index,df_reindex.values)
    for k,v in zip(df_reindex.index,df_reindex.values):
        print('state k:',k,'v:',v,type(v[0]))
    datas = [(k,int(v[0])) for k,v in zip(df_reindex.index,df_reindex.values)]
    print('type datas resolution:',type(datas),datas)

    p = (
        Pie(init_opts=opts.InitOpts(width='720px', height='320px')) #指定画布大小
        .add(series_name=''
            ,data_pair=datas #遍历数据
            ,radius=['35%', '65%'] # 内外半径大小
            ,center=['50%', '50%'] # 圆心位置
        ) 
        .set_global_opts(
            title_opts=opts.TitleOpts(title="eService Issues State",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #添加主、副标题
            ,legend_opts=opts.LegendOpts(pos_bottom="top",orient="horizontal",item_height=7,item_gap = 2,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white',font_size=8)) #设置图例Legend位置
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}({c}):{d}%")) #添加数据标签 
        .set_colors([color_open,color_inprogress,color_reopened,color_resolved,color_closed])  
    )
    return p

@app.route("/unsresolvedCRIssuesOwner")
def unresolved_CR_Issues_Owner():
    p = pie_unresolved_cr_issues_owner()
    return p.dump_options_with_quotes()

def pie_unresolved_cr_issues_owner() -> Pie:
    print('pie_unresolved_cr_issues_owner')
    #owners = ['SKW', 'MTK'] 
    #counts = [50,40]
    series_datas = df_cr_unresolved_owner.value_counts()
    print('series_datas owner:',series_datas)
    order = ['Customer', 'Mediatek']
    df_reindex = pd.DataFrame(series_datas).loc[order]#按order重新排序
    #print('df_reindex:',type(df_reindex),df_reindex.index,df_reindex.values)
    for k,v in zip(df_reindex.index,df_reindex.values):
        print('owner k:',k,'v:',v,type(v))
    datas = [(k,int(v[0])) for k,v in zip(df_reindex.index,df_reindex.values)]
    print('type datas owenr:',type(datas),datas)
    p = (
        Pie(init_opts=opts.InitOpts(width='720px', height='320px')) #指定画布大小
        .add(series_name=''
            ,data_pair=datas #遍历数据
            ,radius=['35%', '65%'] # 内外半径大小
            ,center=['50%', '50%'] # 圆心位置
        ) 
        .set_global_opts(
            title_opts=opts.TitleOpts(title="eService Issues Owner",subtitle=" ",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #添加主、副标题
            ,legend_opts=opts.LegendOpts(pos_bottom="top",orient="horizontal",item_height=7,item_gap = 2,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white',font_size=8)) #设置图例Legend位置
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}({c}):{d}%")) #添加数据标签   
        .set_colors([color_skw,color_mtk])
    )
    return p

@app.route("/allCRIssuesResolutionStatus")
def all_CR_Issues_Resolution_Status():
    print('allCRIssuesStatus')
    b = pie_all_cr_issues_resolution_status()
    return b.dump_options_with_quotes()

def pie_all_cr_issues_resolution_status() -> Pie:
    print('pie_all_cr_issues_resolution_status')
    #status = ['Completed', 'Rejected', 'Not reproducible','Duplicated','Inprogress'] 
    #counts = [50,40,10,30,60]
    #datas = [(o,c) for o,c in zip(status, counts)]
    #[('Inprogress', 57), ('Rejected', 88), ('Not reproducible', 77), ('Duplicated', 29), ('Completed', 252)]
    print('df_cr_resolution:',df_cr_resolution.fillna('Inprogress',inplace=True))
    series_datas = df_cr_resolution.value_counts()
    print('series_datas resolution:',type(series_datas),series_datas)

    order = ['Inprogress', 'Rejected', 'Not reproducible','Duplicated','Completed']
    df_reindex = pd.DataFrame(series_datas).loc[order]#按order重新排序
    #print('df_reindex:',type(df_reindex),df_reindex.index,df_reindex.values)
    for k,v in zip(df_reindex.index,df_reindex.values):
        print('k:',k,'v:',v,type(v[0]))
    datas = [(k,int(v[0])) for k,v in zip(df_reindex.index,df_reindex.values)]
    print('type datas resolution:',type(datas),datas)
    p = (
        Pie(init_opts=opts.InitOpts(width='720px', height='320px')) #指定画布大小
        .add(series_name=''
            ,data_pair=datas #遍历数据
            ,radius=['35%', '65%'] # 内外半径大小
            ,center=['50%', '50%'] # 圆心位置
        ) 
        .set_global_opts(
            title_opts=opts.TitleOpts(title="eService Issues Resolution",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #添加主、副标题
            ,legend_opts=opts.LegendOpts(pos_bottom="top",orient="horizontal",item_height=7,item_gap = 2,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white',font_size=8)) #设置图例Legend位置
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}({c}):{d}%")) #添加数据标签 
        .set_colors([color_open,color_inprogress,color_reopened,color_resolved,color_closed])  
    )
    return p


'''
    eService Issues Solved Daily
'''
@app.route("/crIssuesResolvedDaily")
def all_cr_issues_resolved_daily():
    b = bar_all_cr_issues_daily()
    return b.dump_options_with_quotes()

def bar_all_cr_issues_daily() -> Bar:  # -> 表示要返回的是类型
    series_datas = df_cr_resolved_daily.value_counts().sort_index()
    datas_date = [v[0] for k,v in zip(series_datas.keys(),series_datas.items())] # 遍历series_datas，每次得到一个元素为元组如（'2022-07-13', 1），d[0]为'2022-07-13'，d[1]为1
    datas_resolved = [v[1] for k,v in zip(series_datas.keys(),series_datas.items())]
    print('datas_resolved:',datas_resolved)
    print('datas_date:',datas_date)
    b = (
        Bar()
        .add_xaxis(xaxis_data=datas_date)
        .add_yaxis(series_name=f"Resolved",y_axis=datas_resolved ,color=color_resolved,gap="0",stack='stack1')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="eService Issues Solved Daily",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #设置标题参数
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_height=7,item_gap = 2,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white',font_size=8)) #设置图例Legend参数
            ,xaxis_opts=opts.AxisOpts(name='',name_location='middle',axislabel_opts=opts.LabelOpts(rotate=-45,color='white'))#设置x轴参数
            ,yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='white'))#设置y轴参数
            ,datazoom_opts=opts.DataZoomOpts(type_='inside')
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="insideTop",color="white",font_size="12")) #设置数据标签的参数)
    )
    return b


'''
    eService Issues Solved Weekly
'''
@app.route("/crIssuesResolvedWeekly")
def all_cr_issues_resolved_weekly():
    b = bar_all_cr_issues_weekly()
    return b.dump_options_with_quotes()

def bar_all_cr_issues_weekly() -> Bar:  # -> 表示要返回的是类型
    series_datas = df_cr_resolved_daily.value_counts().sort_index()
    print('series_dats weekly:',series_datas)  
    ''''
    2022-07-13    1
    2022-07-20    1
             ..
    2023-02-21    4
    2023-02-22    1
    '''

    series_datas.index = pd.to_datetime(series_datas.index,format='%Y-%m-%d') #将series自己的index转换成日期类型，以便用Grouper分组
    series_datas = series_datas.groupby(pd.Grouper(freq='W')).sum()
    print('series_datas new:',series_datas)
    series_datas.index = series_datas.index.strftime('%Y-%m-W%W') #重新将timestamp类型转换成str time，['2023-01-W02', '2023-01-W03', ..., '2023-02-W08']

    datas_date = [v[0] for k,v in zip(series_datas.keys(),series_datas.items())] # 遍历series_datas，每次得到一个元素为元组如（'2022-07-13', 1），d[0]为'2022-07-13'，d[1]为1
    datas_resolved = [v[1] for k,v in zip(series_datas.keys(),series_datas.items())]

    print('datas_resolved weekly:',datas_resolved)# [1, 1, 0, 0, 1, 2,... 6, 0, 23, 12, 16, 13]
    print('datas_date weekly:',datas_date) #
    b = (
        Bar(init_opts=opts.InitOpts())
        .add_xaxis(xaxis_data=datas_date)
        .add_yaxis(series_name=f"Resolved",y_axis=datas_resolved ,color=color_resolved)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="eService Issues Solved Weekly",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #设置标题参数
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_height=7,item_gap = 2,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white',font_size=8)) #设置图例Legend参数
            ,xaxis_opts=opts.AxisOpts(name='',name_location='middle',axislabel_opts=opts.LabelOpts(rotate=-30,color='white'))#设置x轴参数
            ,yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='white'))#设置y轴参数
            ,datazoom_opts=opts.DataZoomOpts(type_='inside')
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="insideTop",color="white",font_size="12")) #设置数据标签的参数)
    )
    return b



def loadDatas():
    print("loadData")

    '''
        datas from Issue List  Mediatek eService.cvs
    '''
    global df_cr,submit_date,df_cr_state,df_cr_resolution,df_cr_unresolved_owner,df_cr_resolved_daily
    df_cr = pd.read_csv('Issue List  Mediatek eService.csv')
    submit_date = df_cr['Submit Date'].map(lambda date_str: date_str[0:10]) #取出submit_date这一列并修改，这里取了这一列值的前10个字符，即得到2022-11-29
    #print('submit_date:',submit_date)
    df_cr_state = df_cr['State']
    #print('df_cr_state value_counts:',df_cr_state.value_counts())
    df_cr_resolution = df_cr['Resolution'] #Resolution data
    #print('df_cr_resolution',df_cr_resolution)
    df_cr_unresolved = df_cr[pd.isnull(df_cr['Resolve Date'])] # 没有解决日期的为未打已解决的问题
    #print('df_cr_unresolved:',df_cr_unresolved) 
    df_cr_unresolved_owner = df_cr_unresolved['UserField2'] #owner data
    #print('df_cr_unresolved_owner:',df_cr_unresolved_owner)
    df_cr_resolved_daily = df_cr['Resolve Date'].dropna().astype(str).map(lambda date_str: date_str[0:10]) #dataframe 去掉nan值    


 
if __name__ == '__main__':
    loadDatas()
    
    app.debug = True
    #app.run(host='localhost', port=5000)
    #默认情况下，Flask内置的开发服务器会监听本地机的5000端口，你可以使用127.0.0.1:5000或localhost:5000访问程序
    #app.run()方法运行服务器应用，默认是只能在本机访问的！！！如果需要在其他机器上访问，需要修改为：app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=5000)
