<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="請輸入內容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px"
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
          >{{ "搜索" }}</el-button
        >
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
          >{{ "添加" }}</el-button
        >
      </el-button-group>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
    >
      <el-table-column label="名稱" prop="name"></el-table-column>
      <el-table-column label="類型" prop="type">
        <template slot-scope="{ row }">
          <span>{{ row.type.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="工單流水號前綴"
        prop="ticket_sn_prefix"
      ></el-table-column>
      <el-table-column label="狀態" prop="status" sortable="custom">
        <template slot-scope="{ row }">
          <el-tag v-if="row.status" type="success">啟用</el-tag>
          <el-tag v-else type="danger">禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="查看權限校驗"
        prop="view_permission_check"
        sortable="custom"
      >
        <template slot-scope="{ row }">
          <el-tag v-if="row.view_permission_check" type="success">啟用</el-tag>
          <el-tag v-else type="danger">禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        width="260"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
              >{{ "編輯" }}</el-button
            >
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
              >{{ "刪除" }}</el-button
            >
            <router-link :to="'/wfconf/' + row.id">
              <el-button
                v-if="permissionList.update"
                size="small"
                type="warning"
                >{{ "配置" }}</el-button
              >
            </router-link>
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
        label-width="100px"
        style="width: 400px; margin-left: 50px"
      >
        <el-form-item label="名稱" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="工單號前綴" prop="ticket_sn_prefix">
          <el-input v-model="temp.ticket_sn_prefix" />
        </el-form-item>
        <el-form-item label="工單類型" prop="type">
          <el-select v-model="temp.type" placeholder="請選擇">
            <el-option
              v-for="item in wftype_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="狀態" prop="status">
          <el-switch
            v-model="temp.status"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
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
        <el-form-item label="查看權限校驗" prop="view_permission_check">
          <el-switch
            v-model="temp.view_permission_check"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </el-form-item>
        <el-form-item label="限制表達式" prop="limit_expression">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="限制週期({'period':24} 24小時)"
            v-model="temp.limit_expression"
          />
        </el-form-item>
        <el-form-item label="展現表單字段" prop="display_form_str">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="['name','sn']"
            v-model="temp.display_form_str"
          />
        </el-form-item>
        <el-form-item label="標題模板" prop="title_template">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="你有一個待辦工單:{name}"
            v-model="temp.title_template"
          />
        </el-form-item>
        <el-form-item label="備註" prop="memo">
          <el-input v-model="temp.memo" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ "取消" }}</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
          >{{ "確定" }}</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { workflow, workflowtype, role, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "wfset",

  components: { Pagination },
  data() {
    return {
      valueIdSelectTree: 0,
      propsSelectTree: {
        value: "id",
        label: "name",
        children: "children",
        placeholder: "父級",
      },
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
      },
      temp: {},
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "編輯",
        create: "添加",
      },
      rules: {
        name: [{ required: true, message: "請輸入名稱", trigger: "blur" }],
        type: [{ required: true, message: "請選擇類型", trigger: "change" }],
        ticket_sn_prefix: [
          { required: true, message: "請輸入工單流水號前綴", trigger: "blur" },
        ],
      },
      treeProps: {
        children: "children",
        label: "name",
      },
      treeData: [],
      wftype_list: [],
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
    this.getWftypeList();
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
        .requestMenuButton("wfset")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      workflow.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    getWftypeList() {
      workflowtype.requestGet().then((response) => {
        this.wftype_list = response.results;
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
        name: "",
        ticket_sn_prefix: "xxoo",
        type: "",
        status: true,
        rolse: [],
        view_permission_check: true,
        limit_expression: "",
        display_form_str: "",
        title_template: "",
        content_template: "",
        memo: "",
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
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.temp.roles = this.$refs.tree.getCheckedKeys(true);
          workflow
            .requestPost(this.temp)
            .then((response) => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "創建成功",
                type: "success",
                duration: 2000,
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
      this.temp = row;
      this.temp = Object.assign({}, this.temp, {
        type: this.temp.type.id,
        roles: row.roles.map(a => a.id),
      });
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
        this.$refs.tree.setCheckedKeys(this.temp.roles);
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.loading = true;
          this.temp.roles = this.$refs.tree.getCheckedKeys(true);
          workflow
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000,
              });
              this.getList();
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleDelete(row) {
      this.$confirm("是否確定刪除?", "提示", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          workflow.requestDelete(row.id).then(() => {
            this.$message({
              message: "刪除成功",
              type: "success",
            });
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消刪除",
          });
        });
    },
    getTreeData() {
      role.requestGet().then((response) => {
        this.treeData = this.optionDataSelectTree(response.results);
      });
    },
    optionDataSelectTree(data) {
      const cloneData = data;
      return cloneData.filter((father) => {
        const branchArr = cloneData.filter(
          (child) => father.id === child.parent
        );
        branchArr.length > 0 ? (father.children = branchArr) : "";
        return father.parent === data[0].parent;
      });
    },
  },
};
</script>
