from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

from pyecharts import options as opts
from pyecharts.charts import Bar,Pie,Line

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

app = Flask(__name__,static_folder="templates")

@app.route("/")#使用Flask的 app.route 装饰器将URL路由映射到该函数
def home():
    return render_template("index.html")


def loadDatas():
    print("loadData")

@app.route("/allIssuesPriority")
def all_issues_priority():
    p = pie_all_issues_priority()
    return p.dump_options_with_quotes()

def pie_all_issues_priority() -> Pie:
    owners = ['Blocker', 'Critical', 'Normal'] 
    counts = [50,40,10]
    p = (
        Pie(init_opts=opts.InitOpts(width='300px',height='300px')) #指定画布大小
        .add(series_name=''
            ,data_pair=[(o,c) for o,c in zip(owners, counts)] #遍历数据
            ,radius=['35%', '65%'] # 内外半径大小
            ,center=['50%', '55%'] # 圆心位置
        ) 
        .set_global_opts(
            title_opts=opts.TitleOpts(title="按问题严重等级分布",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #添加主、副标题
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_gap = 5,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white')) #设置图例Legend位置
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%")) #添加数据标签  
        .set_colors([color_blocker,color_critical,color_normal]) 
    )
    return p

@app.route("/skwMtkGoogle")
def skw_mtk_google():
    p = pie_skw_mtk_google()
    return p.dump_options_with_quotes()

def pie_skw_mtk_google() -> Pie:
    owners = ['SKW', 'MTK', 'Google'] 
    counts = [50,40,10]
    p = (
        Pie(init_opts=opts.InitOpts(width='720px', height='320px')) #指定画布大小
        .add(series_name=''
            ,data_pair=[(o,c) for o,c in zip(owners, counts)] #遍历数据
            ,radius=['35%', '65%'] # 内外半径大小
            ,center=['50%', '55%'] # 圆心位置
        ) 
        .set_global_opts(
            title_opts=opts.TitleOpts(title="SKW-MTK-Google 问题",subtitle=" ",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #添加主、副标题
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_gap = 5,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white')) #设置图例Legend位置
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}({c}): {d}%")) #添加数据标签   
        .set_colors([color_skw,color_mtk,color_google])
    )
    return p


@app.route("/allIssuesStatus")
def all_issues_status():
    p = pie_all_issues_status()
    return p.dump_options_with_quotes()

def pie_all_issues_status() -> Pie:
    status = ['Open', 'Inprogress', 'Reopened','Resolved','Closed'] 
    counts = [50,40,10,30,60]
    p = (
        Pie(init_opts=opts.InitOpts(width='720px', height='320px')) #指定画布大小
        .add(series_name=''
            ,data_pair=[(o,c) for o,c in zip(status, counts)] #遍历数据
            ,radius=['35%', '65%'] # 内外半径大小
            ,center=['50%', '55%'] # 圆心位置
        ) 
        .set_global_opts(
            title_opts=opts.TitleOpts(title="按问题解决状态分布",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #添加主、副标题
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_gap = 5,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white')) #设置图例Legend位置
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%")) #添加数据标签 
        .set_colors([color_open,color_inprogress,color_reopened,color_resolved,color_closed])  
    )
    return p


@app.route("/allOwnerIssues")
def all_owner_issues():
    b = bar_all_owner_issues()
    return b.dump_options_with_quotes()

def bar_all_owner_issues() -> Bar:  # -> 表示要返回的是类型
    datas_blocker = [5, 20, 36, 10, 75, 90, 20, 36, 10, 75, 90]
    datas_critical = [15, 25, 16, 55, 48, 8, 25, 16, 55, 48, 8]
    datas_normal = [10, 14, 8, 7, 22, 6, 14, 8, 7, 22, 6]
    datas_eservice = [10, 14, 8, 7, 22, 6, 14, 8, 7, 22, 6]
    datas_owner = ["张三", "李四", "王五", "孙六", "李七", "陈九", "谭一", "陈二", "黄十", "刘十一", "周十二"]
    b = (
        Bar()
        .add_xaxis(xaxis_data=datas_owner)
        .add_yaxis(series_name=f"Blocker({pd.Series(datas_blocker).sum()})"  ,y_axis=datas_blocker ,color=color_blocker   ,gap="0",stack='stack1')
        .add_yaxis(series_name=f"Critical({pd.Series(datas_critical).sum()})",y_axis=datas_critical,color=color_critical ,gap="0",stack='stack1') #gap="0":分组柱状图紧挨着
        .add_yaxis(series_name=f"Normal({pd.Series(datas_normal).sum()})"    ,y_axis=datas_normal  ,color=color_normal  ,gap="0",stack='stack1')
        .add_yaxis(series_name=f"eService({pd.Series(datas_normal).sum()})"  ,y_axis=datas_eservice ,color=color_mtk  ,gap="0")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各Owner问题分布",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #设置标题参数
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_gap = 5,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white')) #设置图例Legend参数
            ,xaxis_opts=opts.AxisOpts(name='',name_location='middle',axislabel_opts=opts.LabelOpts(rotate=-45,color='white'))#设置x轴参数
            ,yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='white'))#设置y轴参数
            ,datazoom_opts=opts.DataZoomOpts(type_='inside')
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="insideTop",color="white",font_size="12")) #设置数据标签的参数)
    )
    return b


@app.route("/allIssuesResolvedStatus")
def issues_resolved_status():
    b = bar_issues_resolved_status()
    return b.dump_options_with_quotes()

def bar_issues_resolved_status() -> Bar:  # -> 表示要返回的是类型
    datas_month = [5, 20, 36, 10, 75, 90,5, 20, 36, 10, 75, 90]
    datas_week = [15, 25, 16, 55, 48, 8,15, 25, 16, 55, 48, 8]
    datas_day = [10, 14, 8, 7, 22, 6,10, 14, 8, 7, 22, 6]
    datas_total = [30, 50, 70, 120, 100, 80,90, 60, 40, 30, 15, 10]
    datas_date = ["2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06","2022-07", "2022-08", "2022-09", "2022-10", "2022-11", "2022-12"]
    line = Line().add_xaxis(datas_date).add_yaxis("Total",y_axis=datas_total)
    b = (
        Bar()
        .add_xaxis(xaxis_data=datas_date)
        .add_yaxis(series_name=f"Month({pd.Series(datas_month).sum()})"  ,y_axis=datas_month ,color="red"   ,gap="0")
        .add_yaxis(series_name=f"Week({pd.Series(datas_week).sum()})",y_axis=datas_week,color="yellow",gap="0") #gap="0":分组柱状图紧挨着
        .add_yaxis(series_name=f"Day({pd.Series(datas_day).sum()})"    ,y_axis=datas_day  ,color="blue"  ,gap="0")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="解题状态跟踪",subtitle="",title_textstyle_opts=opts.TextStyleOpts(font_size=15,color='white')) #设置标题参数
            ,legend_opts=opts.LegendOpts(pos_left="right",orient="vertical",item_gap = 5,inactive_color='grey',textstyle_opts=opts.TextStyleOpts(color='white')) #设置图例Legend参数
            ,xaxis_opts=opts.AxisOpts(name='',name_location='middle',axislabel_opts=opts.LabelOpts(rotate=-45,color='white'))#设置x轴参数
            ,yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='white'))#设置y轴参数
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="insideTop",color="white",font_size="12")) #设置数据标签的参数)
        .overlap(line)
    )
    return b


@app.route("/jiradatas", methods=["GET"])
def jiraDatas():
    return ""

    
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
