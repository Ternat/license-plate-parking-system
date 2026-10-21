<template>
  <el-card shadow="hover" class="card-box">
    <template #header>
      <span style="font-size: 18px; font-weight: bold">Parking Price Management</span>
    </template>

    <div class="manage-content" v-loading="isLoading">
      <el-descriptions title="Current Pricing Rule" :column="1" border style="margin-bottom: 30px">
        <el-descriptions-item label="Free Parking">
          <span style="font-size: 16px; font-weight: bold">{{ freeHours }} hour(s)</span>
        </el-descriptions-item>
        <el-descriptions-item label="Hourly Rate">
          <span style="font-size: 20px; color: #e6a23c; font-weight: bold">
            £ {{ hourlyRate }} / hour
          </span>
        </el-descriptions-item>
        <el-descriptions-item label="Billing Rule">
          Calculate by hours (Real UK Parking Standard)
        </el-descriptions-item>
      </el-descriptions>

      <el-form label-width="180px" style="max-width: 500px; margin: 0 auto">
        <el-form-item label="Free Hours">
          <el-input-number
            v-model="newFreeHours"
            :min="0"
            :step="0.5"
            :max="24"
            style="width: 220px"
          />
        </el-form-item>
        <el-form-item label="New Hourly Rate (£)">
          <el-input-number
            v-model="newRate"
            :min="0.5"
            :step="0.5"
            :max="50"
            style="width: 220px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="savePrice" :loading="isSaving">Save & Apply</el-button>
        </el-form-item>
      </el-form>

      <el-alert
        v-if="showSuccess"
        type="success"
        title="Price saved successfully!"
        style="margin-top: 20px"
        close-text="OK"
        @close="showSuccess = false"
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const hourlyRate = ref(5.0)
const freeHours = ref(2.0)
const newRate = ref(5.0)
const newFreeHours = ref(2.0)
const showSuccess = ref(false)
const isLoading = ref(false)
const isSaving = ref(false)

const loadPricing = async () => {
  isLoading.value = true
  try {
    const res = await request({ url: '/pricing/config', method: 'get' })
    hourlyRate.value = res.data.hourly_rate
    freeHours.value = res.data.free_hours
    newRate.value = res.data.hourly_rate
    newFreeHours.value = res.data.free_hours
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const savePrice = async () => {
  isSaving.value = true
  try {
    await request({
      url: '/pricing/config',
      method: 'put',
      data: { free_hours: newFreeHours.value, hourly_rate: newRate.value }
    })
    hourlyRate.value = newRate.value
    freeHours.value = newFreeHours.value
    showSuccess.value = true
    ElMessage.success(`Updated: Free ${newFreeHours.value}h, £${newRate.value}/hour`)
  } catch (error) {
    console.error(error)
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  loadPricing()
})
</script>

<style scoped>
.card-box {
  max-width: 700px;
  margin: 0 auto;
}
.manage-content {
  padding: 20px;
}
</style>
