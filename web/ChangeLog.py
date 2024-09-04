from app import app, render_template, session, redirect
from flask import jsonify, request
#import json


changelog_data = {
    "v1.2.x":{
        "1.2.0": {
            "date": "20240330",
            "desc": [
                "新增序號驗證",
                "優化彈窗UI"
            ]
        },
        "1.2.1": {
            "date": "20240610",
            "desc": [
                "移除Debug Console"
            ]
        }
    },
    "v1.1.x":{
        "1.1.1": {
            "date": "",
            "desc": [
                "勞作教育_報名：修復<當前人數>為0時,該資料不會被顯示的問題",
                "勞作教育_報名：移除部分棄用的UI"
            ]
        },
        "1.1.2": {
            "date": "",
            "desc": [
                "MainView：修復登出後再次登入,UserID樣式顯示異常的問題"
            ]
        },
        "1.1.3": {
            "date": "20240222",
            "desc": [
                "ScoreQuery：新增即時提取/本地SQL查詢選項"
            ]
        },
        "1.1.4": {
            "date": "20240224",
            "desc": [
                "加密&壓縮算法更動"
            ]
        },
        "1.1.5": {
            "date": "20240304",
            "desc": [
                "門檻總覽：增加懸浮提示",
                "非正式課程：修復只會抓出首欄條件的問題"
            ]
        },
        "1.1.6": {
            "date": "20240314",
            "desc": [
                "門檻總覽：修復錯誤",
                "勞作教育_報名表：修正人數篩選器在初始狀態會有不同步的問題(現預設值為不篩除)",
                "服務學習：新增報名功能",
                "新增：勞作活動自動報名器(預設每10分鐘查詢&嘗試報名,已滿且已預定的活動)"
            ]
        },
        "1.1.7": {
            "date": "20240316",
            "desc": [
                "新增：查詢各科通過率",
                "更新系統優化：解壓流程將在下載完後立即執行,而不是等待所有文件都下載完畢"
            ]
        },
        "1.1.8": {
            "date": "20240327",
            "desc": [
                "應修學分統計：修正不及格分類判定異常問題\n修正修課資料的科目分數檢測,若含徹選或其他非常規狀態時會卡死的問題",
                "LaoZuo_ApplyReserve：修復剩餘時間進度條"
            ]
        },
    }
}

def reverse_changelog_data(data):
    reversed_data = {}
    for version, changes in data.items():
        reversed_data[version] = {k: v for k, v in reversed(changes.items())}
    return reversed_data

reversed_changelog_data = reverse_changelog_data(changelog_data)

@app.route('/ChangeLog')
def ChangeLog():
    return render_template('ChangeLog.html', changelog_data=reversed_changelog_data)

