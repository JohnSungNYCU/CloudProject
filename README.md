# django + vue 工作流管理系统
包含 `使用者`、`角色`、`選單`、`權限` 管理， 這是基礎的工作流程系統，初始化會產生請假工作流程， 也可以自行配置其他工作流程例如，發布工單等。

[comment]: <> (- 后端model参考: [loonflow]&#40;https://github.com/blackholll/loonflow&#41;, 非常不错的一个项目)
[comment]: <> (- 前端设计参考: [花裤衩 vue-element-admin]&#40;https://github.com/PanJiaChen/vue-element-admin&#41;, 大神作品没得说)
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
- Preparation on Ubuntu 20.04
```bash
Setup mysql password must match backend/core/settings/prod.py file settings.
sudo apt-get install npm python3-mysqldb mariadb-server-10.3
sudo mysql -u root -p
CREATE DATABASE one;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password;
SET PASSWORD = PASSWORD('TY%pwd123');
FLUSH PRIVILEGES;
```
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