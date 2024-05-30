<template>
  <div class="navbar">
    <hamburger
      id="hamburger-container"
      :is-active="sidebar.opened"
      class="hamburger-container"
      @toggleClick="toggleSideBar"
    />

    <breadcrumb id="breadcrumb-container" class="breadcrumb-container" />

    <div class="right-menu">
      <template v-if="device !== 'mobile'">
        <div class="right-menu-item">
          <!-- <a class="ip">{{username}}</a> -->
          <a class="date">{{cur_date}}</a>
        </div>

        <search id="header-search" class="right-menu-item" />

        <screenfull id="screenfull" class="right-menu-item hover-effect" />

        <lang-select class="right-menu-item hover-effect" />
      </template>

      <el-dropdown class="avatar-container right-menu-item hover-effect" trigger="click">
        <div class="username">
          {{username}}
          <!-- <el-avatar :src="avatar" /> -->
        </div>
        <el-dropdown-menu slot="dropdown">
          <router-link to="/new_ticket">
            <el-dropdown-item>{{ "新建工單" }}</el-dropdown-item>
          </router-link>
          <router-link to="/my_ticket">
            <el-dropdown-item>{{ "我創建的" }}</el-dropdown-item>
          </router-link>
          <router-link to="/todo_ticket">
            <el-dropdown-item>{{ "我的待辦" }}</el-dropdown-item>
          </router-link>
          <router-link to="/all_ticket">
            <el-dropdown-item>{{ "所有工單" }}</el-dropdown-item>
          </router-link>
          <!-- <el-dropdown-item disabled>{{"個人中心"}}</el-dropdown-item> -->
          <el-dropdown-item divided>
            <span style="display:block;" @click="logout">{{ "登出" }}</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Breadcrumb from "@/components/Breadcrumb";
import Hamburger from "@/components/Hamburger";
import Screenfull from "@/components/Screenfull";
import LangSelect from "@/components/LangSelect";
import Search from "@/components/HeaderSearch";

export default {
  components: {
    Breadcrumb,
    Hamburger,
    Screenfull,
    LangSelect,
    Search
  },
  data() {
    return {
      cur_date: "",
      username: localStorage.getItem('username') || 'nousername',
    };
  },
  computed: {
    ...mapGetters(["sidebar", "name", "avatar", "ip", "device"])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch("app/toggleSideBar");
    },
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    }
  },
  mounted() {
    var _this = this; //聲明一個變量指向vue實例this,保證作用域一致
    this.timer = setInterval(function() {
      _this.cur_date = new Date().toLocaleString(); //修改數據date
    }, 1000);
  }
};
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background 0.3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .errLog-container {
    display: inline-block;
    vertical-align: top;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

        .ip {
          color: #39b3d1;
        }

        .username {
          color: #39b3d1;
        }

        .date {
          color: #d39011;
        }

      &.hover-effect {
        cursor: pointer;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
