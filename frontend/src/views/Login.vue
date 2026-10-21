<template>
  <div class="login-page">
    <div class="login-card">
      <h2 class="login-title">UK Parking Management System</h2>
      <p class="login-subtitle">Administrator Login</p>

      <el-form 
        ref="loginFormRef" 
        :model="loginForm" 
        :rules="loginRules" 
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="Username" 
            size="large"
            :prefix-icon="User" 
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="Password" 
            size="large"
            :prefix-icon="Lock" 
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            class="login-btn" 
            @click="handleLogin"
            :loading="loading"
          >
            Login
          </el-button>
        </el-form-item>
      </el-form>

      <div class="tips">
        Default Account: admin / 123456
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [{ required: true, message: 'Username is required', trigger: 'blur' }],
  password: [{ required: true, message: 'Password is required', trigger: 'blur' }]
}


const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  loading.value = true
  try {
    await loginFormRef.value.validate()
    
    
    const res = await axios.post('http://localhost:8000/api/v1/auth/login', {
      username: loginForm.username,
      password: loginForm.password
    })

    
    const token = res.data.data.access_token
    localStorage.setItem('token', token)
    localStorage.setItem('isLoggedIn', 'true')

    ElMessage.success('Login Success! Redirecting...')
    setTimeout(() => {
      router.push('/recognition')
    }, 500)
    
  } catch (err) {
    ElMessage.error('Invalid Username or Password!')
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  width: 100%;
  height: 100vh;
  background: #f8f9fa; 
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-card {
  width: 420px;
  padding: 40px 30px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08); 
}
.login-title {
  text-align: center;
  font-size: 24px;
  color: #212529;
  margin: 0 0 8px 0;
}
.login-subtitle {
  text-align: center;
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 30px;
}
.login-form { width: 100%; }
.login-btn { width: 100%; height: 44px; font-size: 16px; }
.tips { text-align: center; font-size: 12px; color: #6c757d; margin-top: 20px; }
</style>