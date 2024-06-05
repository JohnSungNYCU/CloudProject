<template>
  <div class="app-container">
    <div class="ticket">
      <el-card>
        <div slot="header" class="clearfix">
          <span class="card-title">流程</span>
        </div>
        <el-steps :active="stateActive" finish-status="success" process-status="finish">
          <el-step v-for="item in state_list" :key="item.id" :title="item.name"></el-step>
        </el-steps>
      </el-card>
      <div class="ticket-form" v-if="customfield_list.length>0">
        <el-form ref="temp" :rules="rules" :model="temp" label-width="100px">
          <el-card>
            <div slot="header" class="card-solt">
              <el-form-item label="工單標題">
                <el-input disabled v-model="this.wfdata.name" />
              </el-form-item>
            </div>
            <el-row :gutter="20">
              <el-col
                :md="{span: [7, 8, 9, 12].includes(item.customfield.field_type)? 22 : 11}"
                v-for="item in customfield_list"
                :key="item.id"
              >
                <el-form-item
                  :label="item.customfield.field_name"
                  :prop="item.field_key"
                  :rules="
                    match_fields.includes(item.customfield.id) && item.field_type !== 15
                      ? [
                          { 
                            required: true, 
                            message: '請輸入' + item.customfield.field_name, 
                            trigger: 'blur' 
                          },
                        ]:[]
                  "
                >
                  <el-input
                    v-if="item.customfield.field_type === 1"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  />

                  <el-input-number
                    v-if="item.customfield.field_type === 2"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-input-number>

                  <el-date-picker
                    type="date"
                    v-if="item.customfield.field_type === 5"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-date-picker>

                  <el-date-picker
                    type="datetime"
                    v-if="item.customfield.field_type === 6"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-date-picker>

                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 4, maxRows: 6}"
                    v-if="item.customfield.field_type === 8"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-input>

                  <el-switch
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    v-if="item.customfield.field_type === 4"
                    v-model="item.field_value"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  ></el-switch>

                  <el-radio-group
                    v-if="item.customfield.field_type === 9"
                    v-model="item.field_value"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-radio
                      v-for="(value, index) in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :label="index"
                    >{{value}}</el-radio>
                  </el-radio-group>

                  <el-checkbox-group
                    v-if="item.customfield.field_type === 12"
                    v-model="item.field_value"
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-checkbox
                      v-for="(value, index)  in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :label="index"
                    >{{value}}</el-checkbox>
                  </el-checkbox-group>

                  <el-select
                    v-if="item.customfield.field_type === 10"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option
                      v-for="(value, index)  in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :value="index"
                    >{{value}}</el-option>
                  </el-select>

                  <el-select
                    v-if="item.customfield.field_type === 13"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    multiple
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option
                      v-for="(value, index)  in JSON.parse(item.customfield.field_choice)"
                      :key="index"
                      :value="index"
                    >{{value}}</el-option>
                  </el-select>

                  <span v-if="item.customfield.field_type === 7">
                    <el-date-picker
                      v-if="item.field_value.length>0"
                      type="datetimerange"
                      :value="formatDate(item.field_value)"
                      :placeholder="item.customfield.field_name"
                      :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                    ></el-date-picker>
                    <el-date-picker
                      v-else
                      type="datetimerange"
                      :value="formatDate(item.field_value)"
                      :placeholder="item.customfield.field_name"
                      :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                    ></el-date-picker>
                  </span>

                  <el-select
                    v-if="item.customfield.field_type === 11"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option v-for="t in user_list" :key="t.id" :label="t.username"></el-option>
                  </el-select>

                  <el-select
                    v-if="item.customfield.field_type === 14"
                    v-model="item.field_value"
                    :placeholder="item.customfield.field_name"
                    clearable
                    multiple
                    :disabled="deny_check || item.participant == username || item.customfield.field_attribute ||! match_fields.includes(item.customfield.id)"
                  >
                    <el-option v-for="t in user_list" :key="t.id" :label="t.username"></el-option>
                  </el-select>

                  <div v-if=" (item.customfield.field_type === 15)">
                    <a 
                      :href="uploadedFileUrl" 
                      :download="uploadedFileName"
                      @click.prevent="downloadFile"
                      class="file-link"
                    >
                      {{ uploadedFileName }}
                    </a>
                  </div>

                </el-form-item>
              </el-col>
            </el-row>
            <div v-if="!deny_check">
              <el-form-item label="審批意見" v-if="stateActive<999">
                <el-input
                  type="textarea"
                  :autosize="{ minRows: 4, maxRows: 6}"
                  v-model="wfdata.memo"
                  placeholder="說些什麼"
                ></el-input>
              </el-form-item>

              <el-form-item>
                <span style="margin: 0 5px;" v-for="item in transition_list" :key="item.id">
                  <el-button
                    v-if="item.name===1"
                    :type="btn_types[item.name]"
                    @click="selectUser('temp', item)"
                  >{{item.name|TransitionNameFilter}}</el-button>
                  <el-button
                    v-else
                    :type="btn_types[item.name]"
                    @click="handleButton('temp', item)"
                  >{{item.name|TransitionNameFilter}}</el-button>
                </span>
              </el-form-item>
            </div>
          </el-card>
        </el-form>
      </div>

      <el-card>
        <div slot="header" class="clearfix">
          <span class="card-title">審批歷史</span>
        </div>
        <el-timeline>
          <el-timeline-item
            v-for="item in ticketlog_list"
            :key="item.id"
            :timestamp="item.create_time"
            icon="el-icon-s-help"
            size="large"
            color="#0bbd87"
            placement="top"
          >
            <el-card class="check_history">
              <div class="check_history_title">
                時間：<a class="state">{{item.create_time}}</a>
                |
                節點：<a class="transition-status">{{item.state.name}}</a>
                |
                操作：<a
                  class="transition-name"
                >{{item.transition.name|TransitionNameFilter}}</a>
              </div>
              <el-form label-position="left">
                <el-form-item label="處理人">
                  <span>{{ item.participant }}</span>
                </el-form-item>
                <el-form-item label="處理意見">
                  <span>{{ item.suggestion }}</span>
                </el-form-item>
              </el-form>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </el-card>
    </div>

    <el-dialog :visible.sync="dialogVisible">
      <div slot="title">
        當前下一步處理對象是：
        <a style="color: red; font-size: 24px">{{
          participant_type[dialogChooiceType]
        }}</a>
        <span v-if="dialogChooiceType==='none'">請直接點確定</span>
        <span v-else>請點選下方處理對象，選擇轉交用戶</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-collapse v-model="dialogChooiceType" accordion @change="selectType">
            <el-collapse-item title="用戶" name="user" disabled></el-collapse-item>
            <el-collapse-item title="部門" name="group" disabled>
              <div v-if="group_role_list.length > 0">
                <li v-for="item in group_role_list" :key="item.id">
                  <el-button
                    style="margin: 2px"
                    size="mini"
                    plain
                    @click="checkGroupUser(item.id)"
                  >
                    {{ item.name }}
                  </el-button>
                </li>
              </div>
              <div v-else>
                沒有可選{{ participant_type[dialogChooiceType] }}
              </div>
            </el-collapse-item>
            <el-collapse-item title="角色" name="role" disabled>
              <div v-if="group_role_list.length > 0">
                <li v-for="item in group_role_list" :key="item.id">
                  <el-button
                    style="margin: 2px"
                    size="mini"
                    plain
                    @click="checkRoleUser(item.id)"
                  >
                    {{ item.name }}
                  </el-button>
                </li>
              </div>
              <div v-else>
                沒有可選{{ participant_type[dialogChooiceType] }}
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-col>
        <el-col :span="16">
          <el-table :data="choice_user_list" @row-click="checkTableUser" style="width: 100%">
            <el-table-column prop="username" label="用户" width="180"></el-table-column>
            <el-table-column prop="realname" label="姓名"></el-table-column>
          </el-table>
        </el-col>
      </el-row>

      <el-row>
        <el-input readonly v-model="wfdata.participant">
          <template slot="prepend">選擇用戶</template>
        </el-input>
      </el-row>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button
          :disabled="wfdata.participant?false:true"
          type="primary"
          @click="handleButton('temp', choice_transition)"
        >確 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  ticketcustomfield,
  state,
  transition,
  ticket,
  ticketflowlog,
  user,
  auth,
} from "@/api/all";
import { mapGetters } from "vuex";
import { getToken } from '@/utils/auth'


export default {
  name: "s_ticket",

  components: {},
  data() {
    return {
      visible: false,
      tempRoute: {},
      wfdata: {},
      customfield_list: [],
      state_list: [],
      transition_list: [],
      ticketlog_list: [],
      user_list: [],
      temp: {},
      rules: {},
      btn_types: {
        0: "primary",
        1: "success",
        2: "warning",
        3: "danger",
        4: "danger",
      },
      match_fields: [],
      workflow_temp: {
        participant: this.username,
        is_hidden: false,
      },
      stateActive: 999,
      choice_user_list: [],
      dialogVisible: false,
      dialogChooiceType: "none",
      participant_list: [],
      choice_transition: {},
      group_role_list: [],
      participant_type: {
        "none": "無處理人",
        "user": "個人",
        "group": "部門",
        "role": "角色",
      },
      deny_check: false, // 允许审核
      fileList: [], // Added for file upload
    };
  },
  computed: {
    ...mapGetters(["username"]),
    formatDate() {
      return function (date) {
        const d = eval("(" + date + ")");
        return d;
      };
    },
    uploadedFileName() {
      return this.$store.state.fileUpload.uploadedFileName;
    },
    uploadedFileUrl() {
      return this.$store.state.fileUpload.uploadedFileUrl;
    },
  },
  created() {
    const id = this.$route.params && this.$route.params.id;
    this.fetchData(id);
    this.getUserList();
    this.tempRoute = Object.assign({}, this.$route);
  },
  methods: {
    fetchData(id) {
      this.workflow_temp.ticket = id;
      const params = {
        id: id,
      };
      ticket.requestGet(params).then((response) => {
        this.wfdata = response.results[0];
        if (this.wfdata.participant !== this.username) {
          this.deny_check = true;
        }
        this.wfdata.memo = "";
        this.setPageTitle();

        this.workflow_temp.workflow = this.wfdata.workflow.id;
        this.workflow_temp.source_state = this.wfdata.state.id;
        this.match_fields = this.wfdata.state.fields;

        this.getCustomfieldList();
        this.getStateList();
        this.getTicketlogList();
      });
    },
    getCustomfieldList() {
      ticketcustomfield.requestGet(this.workflow_temp).then((response) => {
        this.customfield_list = response.results;
      });
    },
    getStateList() {
      state.requestGet(this.workflow_temp).then((response) => {
        this.state_list = response.results;
        for (var i in this.state_list) {
          if (
            this.state_list[i].id == this.wfdata.state.id &&
            this.wfdata.state.state_type < 2
          ) {
            this.stateActive = parseInt(i);
            break;
          }
        }
        this.getTransitionList();
      });
    },
    getTransitionList() {
      transition.requestGet(this.workflow_temp).then((response) => {
        this.transition_list = response.results;
      });
    },
    getTicketlogList() {
      ticketflowlog.requestGet(this.workflow_temp).then((response) => {
        this.ticketlog_list = response.results;
      });
    },
    getUserList() {
      user.requestGet().then((response) => {
        this.user_list = response.results;
      });
    },
    handleFilter() {
      this.fetchData();
    },
    setPageTitle() {
      const title = this.wfdata.name;
      document.title = `${title} - 審批`;
    },
    selectUser(dataForm, row) {
      this.$refs[dataForm].validate((valid) => {
        if (valid) {
          this.dialogVisible = true;
          this.choice_transition = row;
          this.dialogChooiceType = row.dest_state.participant_type;
          this.selectType(this.dialogChooiceType);
        }
      });
    },
    selectType(val) {
      if (val === 'user') {
        this.choice_user_list = this.choice_transition.dest_state.user_participant;
      } else if (val == 'group') {
        this.group_role_list = this.choice_transition.dest_state.group_participant;
      } else if (val == 'role') {
        this.group_role_list = this.choice_transition.dest_state.role_participant;
      } else {
        this.group_role_list = [];
      }
    },
    checkGroupUser(id) {
      const params = {
        group: id,
      };
      user.requestGet(params).then((response) => {
        this.choice_user_list = response.results;
      });
    },
    checkRoleUser(id) {
      const params = {
        roles: id,
      };
      user.requestGet(params).then((response) => {
        this.choice_user_list = response.results;
      });
    },
    checkTableUser(row) {
      this.wfdata.participant = row.username;
    },
    handleButton(dataForm, transition) {
      const customfield = [];
      for (var i of this.customfield_list) {
        customfield.push({
          id: i.id,
          ticket: i.ticket.id,
          customfield: i.customfield.id,
          field_value: i.field_value,
        });
      }
      const data = Object.assign({}, this.wfdata, {
        create_user: this.wfdata.create_user.id,
        workflow: this.wfdata.workflow.id,
        participant: this.wfdata.participant,
        state: transition.dest_state.id,
        transition: transition.id,
        customfield: JSON.stringify(customfield),
        relation: this.username,
      });
      if (transition.name == 1) {
        data.participant = this.wfdata.participant;
        data.relation = this.wfdata.participant;
      } else {
        data.participant = this.ticketlog_list[this.ticketlog_list.length-1].participant;
      }
      this.$refs[dataForm].validate((valid) => {
        if (valid) {
          ticket
            .requestPut(this.wfdata.id, data)
            .then((response) => {
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000,
              });
              this.$router.push({ path: "/todo_ticket" });
            })
            .catch(() => {});
        }
      });
    },
    handlePreview(file) {
      console.log(file);
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    getAuthToken() {
      return getToken(); // This is assuming you have a method to get the token
    },
    async downloadFile() {
      try {
        if (this.uploadedFileUrl) {
          const response = await fetch(this.uploadedFileUrl);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', this.uploadedFileName);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
        } else {
          this.$message.error('File URL not available');
        }
      } catch (error) {
        this.$message.error('Failed to download file. Please try again.');
        console.error('Download error:', error);
      }
    }
  },
};
</script>

<style scoped lang="scss">
.check_history {
  .check_history_title {
    font-weight: 700;
    margin: 10px 0;
    .state {
      color: #0bbd87;
    }
    .transition-status {
      color: #f1bd5f;
    }
    .transition-name {
      color: #f32db1;
    }
  }
  .el-form-item {
    margin-bottom: 5px;
  }
}
.file-link {
  color: #1976d2;  /* Material-UI's primary blue, adjust as needed */
  text-decoration: none;  /* Remove underline by default */
  cursor: pointer;  /* Show pointer cursor on hover */
  font-weight: 500;  /* Makes the link slightly bolder */
}
.file-link:hover {
  text-decoration: underline;  /* Underline on hover */
  color: #1565c0;  /* Slightly darker blue on hover */
}

.file-link:active {
  color: #0d47a1;  /* Even darker blue when clicked */
}

/* Optional: Add a subtle transition for color changes */
.file-link {
  transition: color 0.3s ease;
}

/* Optional: Add an icon before the link */
.file-link::before {
  content: '📄 ';  /* You can use any suitable emoji or icon */
  margin-right: 4px;
}
</style>