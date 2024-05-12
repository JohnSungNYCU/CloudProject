export default {
  systemTitle: '後臺管理系統',

  route: {
    login: '登入',
    dashboard: '首頁',
    sys: '系統管理',
    group: '分組管理',
    user: '用戶管理',
    role: '角色管理',
    menu: '菜單管理',
    icon: '圖標管理',
    tool: '工具管理',
    audit: '審計日誌',
    test: '測試頁面',
    workflow: '工作流',
    wfset: '工作流設計',
    wfconf: '工作流配置',
    wftype: '工作流類型',
    ticket: '工單系統',
    new_ticket: '新建工單',
    u_ticket: '編輯工單',
    s_ticket: '審批工單',
    my_ticket: '我創建的',
    todo_ticket: '我的待辦',
    all_ticket: '所有工單',
    notice: '通知管理',
    mail: 'mail通知',
    telegram: 'telegram通知',
    ComponentDemo: '組件例子'
  },
  navbar: {
    logOut: '退出登入',
    dashboard: '首頁',
    github: '項目地址',
    theme: '換膚',
    size: '布局大小'
  },
  login: {
    title: '系統登入',
    logIn: '登入',
    username: '帳號',
    password: '密碼',
    any: '隨便填',
    thirdparty: '第三方登入',
    thirdpartyTips: '本地不能模擬，請結合自己業務進行模擬!!!'
  },
  documentation: {
    documentation: '文檔',
    github: 'Github 地址'
  },
  permission: {
    addRole: '新增角色',
    editPermission: '編輯權限',
    roles: '你的權限',
    switchRoles: '切換權限',
    tips: '在某些情況下，不適合使用 v-permission。 例如:Element-UI 的 el-tab 或 el-table-column 以及其它動態渲染 dom 的場景。 你只能透過手動設定 v-if 來實現。',
    delete: '刪除',
    confirm: '確定',
    cancel: '取消'
  },
  guide: {
    description: '引導頁對於一些第一次進入專案的人很有用，你可以簡單介紹下項目的功能。本Demo是基於',
    button: '打開引導'
  },
  components: {
    documentation: '文檔',
    tinymceTips: '富文本是管理後台一個核心的功能，但同時又是一個有很多坑的地方。 在選擇富文本的過程中我也走了不少的彎路，市面上常見的富文本都基本上用過了，最終權衡了一下選擇了Tinymce。 更詳細的富文本比較與介紹見',
    dropzoneTips: '由於我司業務有特殊需求，而且要傳七牛 所以沒用第三方，選擇了自己封裝。 程式碼非常的簡單，具體程式碼你可以在這裡看到 @/components/Dropzone',
    stickyTips: '當頁面捲動到預設的位置會吸附在頂部',
    backToTopTips1: '頁面捲動到指定位置會在右下角出現返回頂部按鈕',
    backToTopTips2: '可自訂按鈕的樣式、show/hide、出現的高度、傳回的位置 如需文字提示，可在外部使用Element的el-tooltip元素',
    imageUploadTips: '由於我在使用時它只有vue@1版本，而且和mockjs不相容，所以自己改造了一下，如果大家要使用的話，優先還是使用官方版本。'
  },
  table: {
    dynamicTips1: '固定表頭, 按照表頭順序排序',
    dynamicTips2: '不固定表頭, 按照點擊順序排序',
    dragTips1: '默認順序',
    dragTips2: '拖曳後順序',
    title: '標題',
    importance: '重要性',
    type: '類型',
    remark: '點評',
    search: '搜索',
    add: '添加',
    export: '導出',
    reviewer: '審核人',
    id: '序號',
    date: '時間',
    author: '作者',
    readings: '閱讀數',
    status: '狀態',
    actions: '操作',
    edit: '編輯',
    publish: '發布',
    draft: '草稿',
    delete: '刪除',
    cancel: '取 消',
    confirm: '確 定'
  },
  errorLog: {
    tips: '請點擊右上角bug小圖標',
    description: '現在的管理後台基本上都是spa的形式了，它增強了使用者體驗，但同時也會增加頁面出問題的可能性，可能一個小小的疏忽就導致整個頁面的死鎖。 還好 Vue 官網提供了一個方法來捕捉處理異常，你可以在其中進行錯誤處理或異常上報。',
    documentation: '文檔介紹'
  },
  excel: {
    export: '導出',
    selectedExport: '導出已選擇項',
    placeholder: '請輸入文件名(默認excel-list)'
  },
  zip: {
    export: '導出',
    placeholder: '請輸入文件名(默認file)'
  },
  pdf: {
    tips: '這裡使用   window.print() 來實現下載pdf的功能'
  },
  theme: {
    change: '換膚',
    documentation: '換膚文檔',
    tips: 'Tips: 它區別於 navbar 上的 theme-pick, 是兩種不同的換膚方法，各自有不同的應用場景，具體請參考文件。'
  },
  tagsView: {
    refresh: '刷新',
    close: '關閉',
    closeOthers: '關閉其他',
    closeAll: '關閉所有'
  },
  settings: {
    title: '系統布局配置',
    theme: '主題色',
    tagsView: '開啟 Tags-View',
    fixedHeader: '固定 Header',
    sidebarLogo: '側邊攔 Logo'
  }
}
