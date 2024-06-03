# Fab 測試需求工單管理系統
通過 Vue.js 和 Django 的結合，實現了前後端分離的高效架構。系統包含 `使用者`、`角色`、`選單`、`權限` 管理，初始化工作流程並發布工單。
不僅提供了良好的用戶體驗，還保證了系統的穩定性和安全性。此系統旨在幫助Fab提高測試流程的管理效率，確保測試工作高效有序地進行。

### 參考架構
- 後端: [loonflow] https://github.com/blackholll/loonflow
- 前端: [vue-element-admin] https://github.com/PanJiaChen/vue-element-admin

### 指令
後端
```bash
python manage.py migrate
python manage.py init_sys
python manage.py init_wf
python manage.py init_ticket
python manage.py init_leave
python manage.py runserver
```
## 開發環境
### 後端
安裝依賴
```bash
cd backend
pip install -r dev_requirements.txt
```

初始化系统
- 生成管理員帳號 `admin 123456`
```bash
python manage.py migrate
python manage.py init_sys
```

生成工作流
- 預設使用者帳號 `FabA`,`FabB`,`FabC`,`fab_tl_1`,`fab_tl_2`,`LabA`,`LabB`,`LabC`,`lab_tl_1`,`lab_tl_2`
- 初始密碼皆為 `123456`

```bash
python manage.py init_wf
python manage.py init_ticket
python manage.py init_leave
```

運行
```bash
python manage.py runserver
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## 開始使用
使用 `admin` 登錄，有權限對Fab、Lab與經理帳號作調整或新建帳號。
### 管理人員
![role](https://github.com/itimor/one-workflow/raw/master/gifs/admin.png)

Fab 人員使用創建之帳號登入，並新建工單。
### 新建工單
![role](https://github.com/itimor/one-workflow/raw/master/gifs/ticket_new.png)

### 我創建的
列出由本帳號所建立之委託單 / 工單。
![role](https://github.com/itimor/one-workflow/raw/master/gifs/ticket_my.png)

### 我的待辦
列出等待本帳號處理之委託單 / 工單。
![role](https://github.com/itimor/one-workflow/raw/master/gifs/ticket_todo.png)

### 所有工單
所有的工單列表。
![role](https://github.com/itimor/one-workflow/raw/master/gifs/ticket_all.png)