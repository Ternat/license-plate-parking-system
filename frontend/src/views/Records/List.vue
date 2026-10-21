<template>
  <el-card shadow="hover">
    <template #header>
      <div class="card-header">
        <span style="font-size: 18px; font-weight: bold">UK Parking Records</span>
        <div style="display: flex; gap: 15px">
          <el-input 
            v-model="searchPlate" 
            placeholder="Search by License Plate" 
            style="width: 300px"
            clearable
            @keyup.enter="searchRecords"
          >
            <template #append>
              <el-button :icon="Search" @click="searchRecords" />
            </template>
          </el-input>
          <el-button type="primary" @click="loadAllRecords" :icon="Refresh">
            Refresh
          </el-button>
        </div>
      </div>
    </template>

    <el-table 
      :data="records" 
      style="width: 100%" 
      stripe
      v-loading="isLoading"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="plate_number" label="License Plate" width="180">
        <template #default="{ row }">
          <span style="font-weight: bold; color: #165DFF">{{ row.plate_number }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="entry_time" label="Entry Time" width="200" />
      <el-table-column prop="exit_time" label="Exit Time" width="200">
        <template #default="{ row }">
          {{ row.exit_time || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="parking_duration" label="Duration (h)" width="130">
        <template #default="{ row }">
          {{ row.parking_duration !== null ? row.parking_duration : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="parking_fee" label="Fee (£ GBP)" width="120">
        <template #default="{ row }">
          <span v-if="row.parking_fee !== null" style="font-weight: bold; color: #e6a23c">
            £{{ row.parking_fee }}
          </span>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="Status" width="120">
        <template #default="{ row }">
          <el-tag :type="row.status === 'IN' ? 'success' : 'info'">
            {{ row.status === 'IN' ? 'Parked' : 'Exited' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :total="total"
      layout="total, sizes, prev, pager, next, jumper"
      style="margin-top: 20px; justify-content: flex-end"
      @size-change="loadAllRecords"
      @current-change="loadAllRecords"
    />
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import { getAllRecords, getRecordsByPlate } from '@/api/records'

const records = ref([])
const isLoading = ref(false)
const searchPlate = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadAllRecords = async () => {
  isLoading.value = true
  try {
    const response = await getAllRecords((currentPage.value - 1) * pageSize.value, pageSize.value)
    records.value = response.data.items
    total.value = response.data.total
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const searchRecords = async () => {
  if (!searchPlate.value.trim()) {
    loadAllRecords()
    return
  }
  
  isLoading.value = true
  try {
    const response = await getRecordsByPlate(searchPlate.value.trim())
    records.value = response.data
    total.value = response.data.length
    ElMessage.success(`Found ${response.data.length} records for plate ${searchPlate.value}`)
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadAllRecords()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>