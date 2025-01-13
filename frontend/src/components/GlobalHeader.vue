<template>
  <header class="global-header">
    <div class="logo-container">
      <img src="../assets/logo.svg" alt="Logo" class="logo" />
      <span class="app-name">Annotation Tool</span>
    </div>
    <nav>
      <el-menu mode="horizontal" :default-active="$route.path" router>
        <el-menu-item
          v-for="route in filteredRoutes"
          :key="route.path"
          :index="route.path"
        >
          {{ route.name }}
        </el-menu-item>
      </el-menu>
    </nav>
    <div class="user-section" v-if="userName">
      <span class="user-greeting">Hello, {{ userName }}</span>
      <el-button class="logout-button" type="text" @click="handleLogout">
        Logout
      </el-button>
    </div>
    <el-dialog
      v-model="showUsernameDialog"
      title="Welcome"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
      width="30%"
    >
      <el-form :model="form" @submit.prevent="handleSubmit">
        <el-form-item
          label="Username"
          :rules="[{ required: true, message: 'Username is required' }]"
        >
          <el-input
            v-model="form.username"
            placeholder="Please enter your username"
            @keyup.enter="handleSubmit"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="handleSubmit"> Confirm </el-button>
        </span>
      </template>
    </el-dialog>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";

const router = useRouter();
const store = useStore();

const showUsernameDialog = ref(false);
const form = ref({
  username: "",
});

const filteredRoutes = computed(() => {
  return router.options.routes.filter((route) => route.name);
});

const userName = computed(() => store.state.user.username);

const handleSubmit = () => {
  if (!form.value.username.trim()) {
    ElMessage.warning("Please enter a username");
    return;
  }
  store.commit("user/setUsername", form.value.username.trim());
  showUsernameDialog.value = false;
};

const handleLogout = () => {
  store.dispatch("user/clearUsername");
  showUsernameDialog.value = true;
};

onMounted(() => {
  // If there is no username, show the dialog
  if (!userName.value) {
    showUsernameDialog.value = true;
  }
});
</script>

<style scoped>
.global-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  height: 60px;
  margin-bottom: 0;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px;
  margin-right: 10px;
}

.app-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

nav {
  flex-grow: 1;
  margin-left: 50px;
}

.el-menu {
  background-color: transparent;
  border-bottom: none;
}

.el-menu-item {
  color: #333;
  font-size: 16px;
}

.el-menu-item.is-active {
  color: #409eff;
}

.user-greeting {
  margin-left: auto;
  font-size: 16px;
  color: #333;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.user-greeting {
  font-size: 16px;
  color: #333;
}

.logout-button {
  color: #666;
  font-size: 14px;
}

.logout-button:hover {
  color: #409eff;
}
</style>
