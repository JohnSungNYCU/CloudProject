<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button-group>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >{{ "添加" }}</el-button>
      </el-button-group>
    </div>

    <el-table :data="list" border style="width: 100%" highlight-current-row>
      <el-table-column label="名稱" prop="field_name"></el-table-column>
      <el-table-column label="標識" prop="field_key"></el-table-column>
      <el-table-column label="類型" prop="field_type">
        <template slot-scope="{ row }">
          <span>{{row.field_type|FieldTypeFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="字段是否內置" prop="field_attribute">
        <template slot-scope="{ row }">
          <el-tag v-if="row.field_attribute" type="success">是</el-tag>
          <el-tag v-else type="danger">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="排序" prop="order_id"></el-table-column>
      <el-table-column label="默認值" prop="default_value"></el-table-column>
      <el-table-column label="標籤" prop="label"></el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group v-if="!row.field_attribute">
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >{{ "編輯" }}</el-button>
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >{{ "刪除" }}</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
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
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="字段名稱" prop="field_name">
          <el-input v-model="temp.field_name" />
        </el-form-item>
        <el-form-item label="字段標識" prop="field_key">
          <el-input v-model="temp.field_key" />
          <a class="tips">字段類型請儘量特殊，避免與系統中關鍵字衝突</a>
        </el-form-item>
        <el-form-item label="字段類型" prop="field_type">
          <el-select v-model="temp.field_type" clearable placeholder="請選擇">
            <el-option
              v-for="(label, value) in field_types"
              :key="value"
              :label="label"
              :value="parseInt(value)"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="order_id">
          <el-input v-model="temp.order_id" />
        </el-form-item>
        <el-form-item label="默認值" prop="default_value">
          <el-input v-model="temp.default_value" />
          <a class="tips">前端展示時，可以將此內容作為表單中的該字段的默認值</a>
        </el-form-item>
        <el-form-item label="文本域模板" prop="field_template" v-if="temp.field_type===9">
          <el-input v-model="temp.field_template" />
          <a class="tips">文本域類型字段前端顯示時可以將此內容作為字段的placeholder</a>
        </el-form-item>
        <el-form-item label="布爾類型顯示名" prop="boolean_field_display" v-if="temp.field_type===4">
          <el-input v-model="temp.boolean_field_display" />
          <a class="tips">當為布爾類型時候，可以支持自定義顯示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意數字也需要引號</a>
        </el-form-item>
        <el-form-item label="多選值" prop="field_choice" v-if="[9,10,12,13].includes(temp.field_type)">
          <el-input v-model="temp.field_choice" />
          <a class="tips">radio,select:{"1":"中國", "2":"美國"},注意數字也需要引號</a>
        </el-form-item>
        <el-form-item label="標籤" prop="label">
          <el-input v-model="temp.label" />
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
        >{{ "確定" }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { customfield, auth } from "@/api/all";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "customfield",
  props: {
    wfdata: {
      type: Object,
      default: {}
    },
    list: {
      type: Array,
      default: []
    }
  },

  components: {},
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false
      },
      temp: {},
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "編輯",
        create: "添加"
      },
      rules: {
        name: [{ required: true, message: "請輸入名稱", trigger: "blur" }]
      },
      field_types: {
        1: "字符串",
        2: "整形",
        3: "浮點型",
        4: "布爾",
        5: "日期",
        6: "日期時間",
        7: "範圍日期",
        8: "文本域",
        9: "單選框",
        10: "下拉列表",
        11: "用戶名",
        12: "多選框",
        13: "多選下拉",
        14: "多選用戶名"
      }
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
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
        .requestMenuButton("customfield")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    handleFilter() {},
    resetTemp() {
      this.temp = {
        memo: "",
        field_type: 1,
        field_key: "",
        field_name: "",
        order_id: 10,
        default_value: "",
        field_template: "",
        boolean_field_display: "",
        field_choice: "",
        label: "",
        workflow: this.wfdata.id
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          customfield
            .requestPost(this.temp)
            .then(response => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "創建成功",
                type: "success",
                duration: 2000
              });
              this.$emit("checkdata");
            })
            .catch(() => {});
        }
      });
    },
    handleUpdate(row) {
      this.temp = row;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          customfield
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000
              });
              this.$emit("checkdata");
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
        type: "warning"
      })
        .then(() => {
          customfield.requestDelete(row.id).then(() => {
            this.$message({
              message: "刪除成功",
              type: "success"
            });
            this.$emit("checkdata");
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
