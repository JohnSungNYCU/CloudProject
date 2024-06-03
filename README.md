# Fab 測試需求工單管理系統
通過 Vue.js 和 Django 的結合，實現了前後端分離的高效架構。系統包含 `使用者`、`角色`、`選單`、`權限` 管理，初始化工作流程並發布工單。
不僅提供了良好的用戶體驗，還保證了系統的穩定性和安全性。此系統旨在幫助Fab提高測試流程的管理效率，確保測試工作高效有序地進行。

### 參考架構
- 後端: [loonflow]&#40;https://github.com/blackholll/loonflow&#41;
- 前端: [vue-element-admin]&#40;https://github.com/PanJiaChen/vue-element-admin&#41;

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
- 用戶 `ops`,`ops_tl`,`dev`,`dev_tl`,`hr`,`hr_tl`
- 密碼 `123456`

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
使用 `admin` 登陸
### 給所有角色分配工作流程權限
![role](https://github.com/itimor/one-workflow/raw/master/gifs/role.png)

### 分配選單 和 資料 權限
![role_edit](https://github.com/itimor/one-workflow/raw/master/gifs/role_edit.png)

### 配置假期工作流
![role](https://github.com/itimor/one-workflow/raw/master/gifs/leave.png)

### 新建工單
![role](https://github.com/itimor/one-workflow/raw/master/gifs/new.png)

### 編輯工單
![role](https://github.com/itimor/one-workflow/raw/master/gifs/edit.png)

### 所有工單
![role](https://github.com/itimor/one-workflow/raw/master/gifs/all.png)