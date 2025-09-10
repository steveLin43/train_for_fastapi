參考內容: [FastAPI 開發筆記：從新手到專家的成長之路](https://ithelp.ithome.com.tw/articles/10318219)

安裝套件:
pip install "fastapi[all]"
pip install "uvicorn[standard]"
pip install python-multipart
pip install sqlalchemy
pip install alembic

查看文件:
直接到 http://127.0.0.1:8000/docs
或是 http://127.0.0.1:8000/redoc

資料庫初始化(migration):
1. 產生設定檔: alembic init testAlembic
2. 進入 alembic.ini 檔案內修改 sqlalchemy.url
3. 開始手動建立: alembic revision -m "create user table"
4. 手動調整新增的檔案內容，更新 upgrade() 和 downgrade() 內的內容

注意事項:
1. 沒有指定是 Form 物件的話，FastAPI 會認定是 Query Parameter
2. 如果沒有用 summary 參數，function 名稱會成為文件中後面的說明