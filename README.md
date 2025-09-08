參考內容: [FastAPI 開發筆記：從新手到專家的成長之路](https://ithelp.ithome.com.tw/articles/10318219)

安裝套件:
pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart

查看文件:
直接到 http://127.0.0.1:8000/docs
或是 http://127.0.0.1:8000/redoc


注意事項:
1. 沒有指定是 Form 物件的話，FastAPI 會認定是 Query Parameter
2. 如果沒有用 summary 參數，function 名稱會成為文件中後面的說明