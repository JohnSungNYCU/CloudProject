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
      <el-table-column label="菜單名稱" prop="name"></el-table-column>
      <el-table-column label="菜單代碼" prop="code"></el-table-column>
      <el-table-column label="排序值" prop="sequence"></el-table-column>
      <el-table-column label="菜單類型" prop="type">
        <template slot-scope="{ row }">
          <span>{{ row.type | menuTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作類型" prop="operate">
        <template slot-scope="{ row }">
          <span>{{ row.operate | operateTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="菜單狀態" prop="status">
        <template slot-scope="{ row }">
          <span>{{row.status}}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group v-show="row.id !== 1">
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
        <el-form-item label="父級" prop="parent">
          <SelectTree
            v-model.number="temp.parent"
            type="number"
            :props="propsSelectTree"
            :options="optionDataSelectTree"
            :value="valueIdSelectTree2"
            :clearable="true"
            :accordion="true"
            @getValue="getSelectTreeValue($event, 2)"
          />
        </el-form-item>
        <el-form-item label="菜單名稱" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="菜單代碼" prop="code">
          <el-input v-model="temp.code" />
        </el-form-item>
        <el-form-item label="菜單URL" prop="curl">
          <el-input v-model="temp.curl" />
        </el-form-item>
        <el-form-item label="菜單圖標" prop="icon">
          <el-input v-model="temp.icon" />
        </el-form-item>
        <el-form-item label="排序值" prop="sequence">
          <el-input v-model="temp.sequence" />
        </el-form-item>
        <el-form-item label="菜單類型" prop="type">
          <el-select
            v-model.number="temp.type"
            placeholder="狀態"
            style="width: 90px"
            @change="handleshowOpera"
          >
            <el-option
              v-for="item in menuTypeOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
        </el-form-item>
        <el-form-item v-show="showOpera" label="操作類型" prop="operate">
          <el-select
            v-model="temp.operate"
            placeholder="狀態"
            style="width: 90px"
            class="filter-item"
          >
            <el-option
              v-for="item in operateTypeOptions"
              :key="item.key"
              :label="item.display_name"
              :value="item.key"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="菜單狀態" prop="status">
          <el-switch v-model="temp.status" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="是否緩存" prop="no_cache">
          <el-switch v-model="temp.no_cache" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="隱藏菜單" prop="hidden">
          <el-switch v-model="temp.hidden" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
        </el-form-item>
        <el-form-item label="激活菜單" prop="active_menu">
          <el-input v-model="temp.active_menu" />
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
import { menu, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import SelectTree from "@/components/TreeSelect";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "ymenu",

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
        name: [{ required: true, message: "請輸入名稱", trigger: "blur" }],
        sequence: [{ required: true, message: "請輸入排序", trigger: "blur" }]
      },
      multipleSelection: [],
      treeProps: {
        children: "children",
        label: "name"
      },
      treeData: [],
      menuTypeOptions: [
        { key: 1, display_name: "模塊" },
        { key: 2, display_name: "菜單" },
        { key: 3, display_name: "操作" }
      ],
      operateTypeOptions: [
        { key: "none", display_name: "無" },
        { key: "add", display_name: "新增" },
        { key: "del", display_name: "刪除" },
        { key: "update", display_name: "編輯" },
        { key: "view", display_name: "查看" }
      ],
      showOpera: false,
      allmean: []
    };
  },
  computed: {
    optionDataSelectTree() {
      const cloneData = this.allmean;
      return cloneData.filter(father => {
        const branchArr = cloneData.filter(child => father.id === child.parent);
        branchArr.length > 0 ? (father.children = branchArr) : "";
        return father.parent === this.allmean[0].parent;
      });
    }
  },
  created() {
    this.getMenuButton();
    this.getList();
    this.getAllMean();
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
        .requestMenuButton("menu")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      menu.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    getAllMean() {
      menu.requestGet().then(response => {
        this.allmean = response.results;
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
        code: "",
        curl: "",
        icon: "list",
        sequence: "",
        type: 2,
        operate: "none",
        status: true,
        no_cache: true,
        hidden: false,
        active_menu: "",
        parent: 0
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
          this.temp.parent = this.valueIdSelectTree2;
          menu
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
      this.temp = row;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.valueIdSelectTree2 = this.temp.parent;
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          this.loading = true;
          this.temp.parent = this.valueIdSelectTree2;
          menu
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
      menu.requestDelete(row.id).then(() => {
        this.$message({
          message: "刪除成功",
          type: "success"
        });
        this.getList();
      });
    },
    handleshowOpera(val) {
      if (val === 3) {
        this.showOpera = true;
      } else {
        this.showOpera = false;
        this.temp.operate = "none";
      }
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
          menu.requestBulkDelete(ids).then(response => {
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
    }
  }
};
</script>
