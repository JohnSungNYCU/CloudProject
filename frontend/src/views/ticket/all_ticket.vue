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
        <!-- <el-button
          v-if="permissionList.del & (username === 'admin')"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
          >{{ "刪除" }}</el-button
        > -->
      </el-button-group>
      <el-radio-group
        class="filter-item"
        text-color="#db5a6b"
        fill="#ffc773"
        v-model="listQuery.transition__attribute_type"
        @change="getList"
      >
        <el-radio-button
          v-for="(item, index) in attribute_types"
          :key="index"
          :label="index"
        >{{item}}</el-radio-button>
      </el-radio-group>
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
      <el-table-column
        v-if="username === 'admin'"
        type="selection"
        width="55"
      />
      <el-table-column label="名稱" prop="name"></el-table-column>
      <el-table-column label="單號" prop="sn" width="240">
        <template slot-scope="{ row }">
          <router-link :to="'/s_ticket/' + row.id">
            <el-link type="success">{{ row.sn }}</el-link>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column label="申請人" prop="create_user">
        <template slot-scope="{ row }">
          <span>{{ row.create_user.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="當前環節" prop="state">
        <template slot-scope="{ row }">
          <span>{{ row.state.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="急件狀態" prop="transition">
        <template slot-scope="{ row }">
          <span>
          {{
            JSON.parse(row.customfield).find(item => item.field_key === 'status' || item.customfield % 10 === 7).field_value | AttributeTypeFilter2
          }}
          </span>
      </template>
      </el-table-column>
      <el-table-column label="當前處理人" prop="participant">
        <template slot-scope="{ row }">
          <span>{{ row.participant }}</span>
        </template>
      </el-table-column>
      <el-table-column label="創建日期" prop="create_time"></el-table-column>
      <!-- <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.del && row.state.order_id < 3"
              size="small"
              type="danger"
              @click="handleDelete(row)"
              >{{ "刪除" }}</el-button
            >
          </el-button-group>
        </template>
      </el-table-column> -->
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
  </div>
</template>

<script>
import { ticket, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";
import { mapGetters } from "vuex";

export default {
  name: "all_ticket",

  components: { Pagination },
  data() {
    return {
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
        transition__attribute_type: "",
      },
      multipleSelection: [],
      attribute_types: {
        '': "全部",
        0: "草稿",
        1: "待審",
        2: "駁回",
        3: "撤銷",
        4: "結束",
        5: "已關閉",
      },
    };
  },
  computed: {
    ...mapGetters(["username"]),
  },
  created() {
    this.getMenuButton();
    this.getList();
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
        .requestMenuButton("all_ticket")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      ticket.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
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
    handleDelete(row) {
      this.$confirm("是否確定刪除?", "提示", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          ticket.requestDelete(row.id).then(() => {
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
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleBatchDel() {
      if (this.multipleSelection.length === 0) {
        this.$message({
          message: "未選中任何行",
          type: "warning",
          duration: 2000,
        });
        return;
      }
      this.$confirm("是否確定刪除?", "提示", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          const ids = this.multipleSelection.map((x) => x.id);
          ticket.requestBulkDelete(ids).then((response) => {
            console.log(response.results);
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
  },
};
</script>
