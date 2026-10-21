<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" style="background-color: #2f4050">
      <div style="color: white; text-align: center; padding: 25px 0; font-size: 18px; font-weight: bold; border-bottom: 1px solid #1f2d3d">
        UK LPR System
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#2f4050"
        text-color="#a7b1c2"
        active-text-color="#1ab394"
        style="border: none"
      >
        <el-menu-item index="/recognition">
          <el-icon><Search /></el-icon>
          <span>License Plate Recognition</span>
        </el-menu-item>
        <el-menu-item index="/parking/entry">
          <el-icon><CirclePlus /></el-icon>
          <span>Vehicle Entry</span>
        </el-menu-item>
        <el-menu-item index="/parking/exit">
          <el-icon><CircleClose /></el-icon>
          <span>Vehicle Exit</span>
        </el-menu-item>
        <el-menu-item index="/records">
          <el-icon><Document /></el-icon>
          <span>Parking Records</span>
        </el-menu-item>
        <el-menu-item index="/parking/price">
          <el-icon><Money /></el-icon>
          <span>Price Management</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background-color: white; border-bottom: 1px solid #e6e6e6; display: flex; align-items: center; justify-content: space-between; padding: 0 30px">
        <span style="font-size: 20px; font-weight: bold; color: #2f4050">{{ currentTitle }}</span>
        <div class="header-right">
          <span style="margin-right:15px;color:#999">
            <el-icon><Clock /></el-icon> {{ currentTime }}
          </span>
          
          <el-button type="danger" size="small" @click="handleLogout">Logout</el-button>
        </div>
      </el-header>
      <el-main style="background-color: #f3f3f4; padding: 25px">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const activeMenu = computed(() => route.path)
const currentTitle = computed(() => route.meta.title || 'UK LPR Parking System')
const currentTime = ref('')
let timer = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('en-US')
}


const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('isLoggedIn')
  ElMessage.success('Logout Successful!')
  router.push('/login')
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.el-header {
  height: 60px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>