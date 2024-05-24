<template>
  <div class="app-container">
    <h1>這是一個測試頁面</h1>
    <h3>下面是你對這個頁面的相關操作權限，如果沒有，則不會顯示相應的按鈕</h3>
    <el-button v-if="permissionList.add" size="small" type="primary">
      {{ "增加" }}
    </el-button>

    <el-button v-if="permissionList.del" size="small" type="danger">
      {{ "刪除" }}
    </el-button>

    <el-button v-if="permissionList.update" size="small" type="warning">
      {{ "編輯" }}
    </el-button>

    <el-button v-if="permissionList.view" size="small" type="success">
      {{ "查看" }}
    </el-button>
  </div>
</template>

<script>
  import {auth} from '@/api/all'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'

  export default {
    name: 'test',
    data() {
      return {
        operationList: [],
        permissionList: {
          add: false,
          del: false,
          view: false,
          update: false
        }
      }
    },
    created() {
      this.getMenuButton()
    },
    methods: {
      checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
      },
      getMenuButton() {
        auth.requestMenuButton('test').then(response => {
          this.operationList = response.results
        }).then(() => {
          this.checkPermission()
        })
      },
    }
  }
</script>
