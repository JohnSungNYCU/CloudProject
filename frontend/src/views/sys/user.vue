  <template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="請輸入內容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button-group>
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="handleFilter"
        >{{ "搜索" }}</el-button>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >{{ "添加" }}</el-button>
        <el-button
          v-if="permissionList.del"
          :disabled="multipleSelection.length<1"
          class="filter-item"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
        >{{ "刪除" }}</el-button>
      </el-button-group>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column label="用戶名" prop="username"></el-table-column>
      <el-table-column label="真實姓名" prop="realname"></el-table-column>
      <!-- <el-table-column label="頭像" align="center">
        <template slot-scope="{ row }">
          <el-popover placement="top" width="200" trigger="hover">
            <el-image :src="row.avatar" fit="cover"></el-image>
            <el-avatar slot="reference" :src="row.avatar"></el-avatar>
          </el-popover>
        </template>
      </el-table-column> -->
      <el-table-column label="狀態" prop="status" sortable="custom">
        <template slot-scope="{ row }">
          <el-tag v-if="row.status" type="success">啟用</el-tag>
          <el-tag v-else type="danger">禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group v-show="!row.is_admin">
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >{{ "編輯" }}</el-button>
            <el-popconfirm title="你確定要刪除嗎" @onConfirm="handleDelete(row)">
              <el-button
                slot="reference"
                v-if="permissionList.del"
                size="small"
                type="danger"
              >{{ "刪除" }}</el-button>
            </el-popconfirm>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="用戶名" prop="username">
          <el-input v-model="temp.username" :disabled="dialogStatus === 'create' ? false : true" />
        </el-form-item>
        <el-form-item v-if="dialogStatus === 'create' ? true : false" label="密碼" prop="password">
          <el-input
            v-model="temp.password"
            placeholder="6-20位"
            show-password
            minlength="6"
            maxlength="20"
          />
        </el-form-item>
        <el-form-item label="真實姓名" prop="realname">
          <el-input v-model="temp.realname" />
        </el-form-item>
        <el-form-item label="分組" prop="realname">
          <SelectTree
            v-model.number="temp.group"
            type="number"
            :props="propsSelectTree"
            :options="optionDataSelectTree2"
            :value="valueIdSelectTree2"
            :clearable="true"
            :accordion="true"
            @getValue="getSelectTreeValue($event, 2)"
          />
        </el-form-item>
        <!-- <el-form-item label="頭像" prop="avatar">
          <el-input v-model="temp.avatar" />
        </el-form-item> -->
        <!-- <el-form-item label="介紹" prop="memo">
          <el-input v-model="temp.memo" />
        </el-form-item> -->
        <el-form-item label="狀態" prop="status">
          <el-switch v-model="temp.status" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="角色" prop="roles">
          <el-tree
            ref="tree"
            :check-strictly="false"
            :data="treeData"
            :props="treeProps"
            show-checkbox
            accordion
            default-expand-all
            node-key="id"
            class="permission-tree"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ "取消" }}</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
        >{{ "確定" }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { user, group, role, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import SelectTree from "@/components/TreeSelect";

import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "user",
  components: { Pagination, SelectTree },
  data() {
    return {
      valueIdSelectTree: 0,
      valueIdSelectTree2: 0,
      propsSelectTree: {
        value: "id",
        label: "name",
        children: "children",
        placeholder: "父級"
      },
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined
      },
      temp: {},
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "編輯",
        create: "添加"
      },
      rules: {
        username: [
          { required: true, message: "請輸入用戶名", trigger: "blur" }
        ],
        password: [
          {
            min: 6,
            max: 20,
            required: true,
            message: "長度在 6 到 20 個字符",
            trigger: "blur"
          }
        ]
      },
      multipleSelection: [],
      treeProps: {
        children: "children",
        label: "name"
      },
      treeData: [],
      allgroup: []
    };
  },
  computed: {
    optionDataSelectTree2() {
      const cloneData = this.allgroup;
      const ha = cloneData.filter(father => {
        const branchArr = cloneData.filter(child => father.id === child.parent);
        branchArr.length > 0 ? (father.children = branchArr) : "";
        return father.parent === this.allgroup[0].parent;
      });
      return ha;
    }
  },
  created() {
    this.getMenuButton();
    this.getList();
    this.getGroupList();
    this.getTreeData();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("user")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      user.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    getGroupList() {
      group.requestGet().then(response => {
        this.allgroup = response.results;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    },
    resetTemp() {
      this.temp = {
        username: "",
        password: "",
        realname: "",
        group: "",
        avatar:
          "http://m.imeitou.com/uploads/allimg/2017110610/b3c433vwhsk.jpg",
        roles: [],
        status: true,
        memo: ""
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.loading = false;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          this.loading = true;
          this.temp.group = this.valueIdSelectTree2;
          this.temp.roles = this.$refs.tree.getCheckedKeys(true);
          user
            .requestPost(this.temp)
            .then(response => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "創建成功",
                type: "success",
                duration: 2000
              });
              this.getList();
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleUpdate(row) {
      // this.temp = Object.assign({},row, {
      //   group: row.group.id,
      //   roles: row.roles.map(a => a.id),
      // });
      this.temp = row;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
        this.valueIdSelectTree2 = this.temp.group;
        this.$refs.tree.setCheckedKeys(this.temp.roles);
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          this.loading = true;
          this.temp.group = this.valueIdSelectTree2;
          this.temp.roles = this.$refs.tree.getCheckedKeys(true);
          user
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000
              });
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleDelete(row) {
      user.requestDelete(row.id).then(() => {
        this.$message({
          message: "刪除成功",
          type: "success"
        });
        this.getList();
      });
    },
    getSelectTreeValue(value, type) {
      if (type === 1) {
        this.valueIdSelectTree = value;
        this.handleFilter();
      } else {
        this.valueIdSelectTree2 = value;
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleBatchDel() {
      this.$confirm("是否確定刪除?", "提示", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          const ids = this.multipleSelection.map(x => x.id);
          user.requestBulkDelete(ids).then(response => {
            console.log(response.results);
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消刪除"
          });
        });
    },
    getTreeData() {
      role.requestGet().then(response => {
        this.treeData = this.optionDataSelectTree(response.results);
      });
    },
    optionDataSelectTree(data) {
      const cloneData = data;
      return cloneData.filter(father => {
        const branchArr = cloneData.filter(child => father.id === child.parent);
        branchArr.length > 0 ? (father.children = branchArr) : "";
        return father.parent === data[0].parent;
      });
    }
  }
};
</script>
