<template>
  <div class="app-container">
    <el-table
      :data="list"
      v-loading="listLoading"
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
    >
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
      <!-- <el-table-column label="申請人" prop="create_user">
        <template slot-scope="{ row }">
          <span>{{ row.create_user.username }}</span>
        </template>
      </el-table-column> -->
      <el-table-column label="創建日期" prop="create_time"></el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              size="small"
              icon="el-icon-arrow-up"
              @click.stop="handleCommand({ action: 'moveUp', row })"
            >上移</el-button>
            <el-button
              size="small"
              icon="el-icon-arrow-down"
              @click.stop="handleCommand({ action: 'moveDown', row })"
            >下移</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
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
  name: "todo_ticket",

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
      listQuery: {
        // offset: 1,
        // limit: 20,
        search: undefined,
        ordering: undefined,
        participant: this.username,
        transition__attribute_type__lt: 4,
      },
      contextMenuVisible: false,
      contextMenuTop: '0px',
      contextMenuLeft: '0px',
      selectedRow: null,
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
        .requestMenuButton("todo_ticket")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      this.listQuery.participant = this.username;
      ticket.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        // 如果 localStorage 中有保存的列表順序，則按照這個順序對列表進行排序
        const listOrder = JSON.parse(localStorage.getItem('listOrder'));
        if (listOrder) {
          this.list.sort((a, b) => listOrder.indexOf(a.id) - listOrder.indexOf(b.id));
        }
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
    handleContextMenu(event) {
        this.contextMenuVisible = true;
        this.contextMenuTop = event.clientY + 'px';
        this.contextMenuLeft = event.clientX + 'px';
        event.stopPropagation();
        event.preventDefault();
      },
      handleCommand(command) {
        this.selectedRow = command.row;
  
        if (command.action === 'moveUp') {
          this.moveUp();
        } else if (command.action === 'moveDown') {
          this.moveDown();
        }
      },
      moveUp() {
        const index = this.list.indexOf(this.selectedRow);
        if (index > 0) {
          const temp = this.list[index];
          this.list.splice(index, 1);
          this.list.splice(index - 1, 0, temp);
        }
        // 將當前的列表順序保存到 localStorage
        localStorage.setItem('listOrder', JSON.stringify(this.list.map(item => item.id)));
      },
      moveDown() {
        const index = this.list.indexOf(this.selectedRow);
        if (index < this.list.length - 1) {
          const temp = this.list[index];
          this.list.splice(index, 1);
          this.list.splice(index + 1, 0, temp);
        }
        // 將當前的列表順序保存到 localStorage
        localStorage.setItem('listOrder', JSON.stringify(this.list.map(item => item.id)));
      },
  },
};
</script>
