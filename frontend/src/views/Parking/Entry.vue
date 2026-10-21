<template>
  <el-card shadow="hover">
    <template #header>
      <div class="card-header">
        <span style="font-size: 18px; font-weight: bold">Vehicle Entry</span>
        <el-switch
          v-model="autoMode"
          active-text="Auto Video Detection"
          inactive-text="Manual Upload"
          @change="resetAll"
        />
      </div>
    </template>

    <el-row :gutter="30">
      <el-col :span="12">
        <div v-if="autoMode" class="camera-box">
          <video 
            ref="videoRef" 
            autoplay 
            muted 
            playsinline 
            class="preview-video"
          ></video>
        </div>


        <div v-else>
          <el-upload
            class="image-uploader"
            :drag="true"
            :auto-upload="false"
            :on-change="handleFileChange"
            :show-file-list="false"
            accept="image/*"
          >
            <el-icon style="font-size: 60px; color: #67c23a"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              Drag image here or click to upload
            </div>
          </el-upload>
        </div>

        <div v-if="previewImage" style="margin-top:20px;text-align:center">
          <el-image 
            :src="previewImage" 
            style="width:100%;max-height:300px;border-radius:8px" 
            fit="contain"
          />
        </div>
      </el-col>

      <el-col :span="12">
        <el-button
          v-if="!autoMode"
          type="success"
          size="large"
          @click="handleEntry"
          :loading="isLoading"
          style="width:100%;height:50px"
        >
          <el-icon><CircleCheck /></el-icon>
          Confirm Entry
        </el-button>

        <el-result v-if="entryResult" icon="success" title="Vehicle Entry Successful">
          <template #sub-title>
            <el-descriptions :column="1" :border="true" :style="{backgroundColor:'white'}">
              <el-descriptions-item label="Plate">{{ entryResult.plate_number }}</el-descriptions-item>
              <el-descriptions-item label="Time">{{ entryResult.entry_time }}</el-descriptions-item>
            </el-descriptions>
          </template>
        </el-result>

        <el-empty v-else-if="!previewImage && !autoMode" description="Upload an image" />
        <el-empty v-else-if="!previewImage && autoMode" description="Auto detection running..." />
      </el-col>
    </el-row>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { vehicleEntry } from '@/api/parking'
import { UploadFilled, CircleCheck } from '@element-plus/icons-vue'

const previewImage = ref('')
const selectedFile = ref(null)
const isLoading = ref(false)
const entryResult = ref(null)
const autoMode = ref(false)

const videoRef = ref(null)
let stream = null
let timer = null

let lastCall = 0
const cooldown = 8000

const resetAll = () => {
  previewImage.value = ''
  selectedFile.value = null
  entryResult.value = null
  stopCamera()
}

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  previewImage.value = URL.createObjectURL(file.raw)
  entryResult.value = null
}

const handleEntry = async () => {
  if (!selectedFile.value) return
  isLoading.value = true
  try {
    const res = await vehicleEntry(selectedFile.value)
    entryResult.value = res.data
  } catch (e) {}
  isLoading.value = false
}
const startAutoDetection = async () => {
  if (stream) stopCamera()
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    videoRef.value.srcObject = stream

    timer = setInterval(() => {
      if (Date.now() - lastCall < cooldown) return
      lastCall = Date.now()

      const canvas = document.createElement('canvas')
      canvas.width = videoRef.value.videoWidth
      canvas.height = videoRef.value.videoHeight
      const ctx = canvas.getContext('2d')
      ctx.drawImage(videoRef.value, 0, 0)

      canvas.toBlob(blob => {
        const file = new File([blob], 'auto.jpg')
        vehicleEntry(file).then(res => {
          entryResult.value = res.data
        })
      })
    }, 500)
  } catch (e) {}
}

const stopCamera = () => {
  clearInterval(timer)
  if (stream) {
    stream.getTracks().forEach(t => t.stop())
    stream = null
  }
}

watch(autoMode, (val) => {
  if (val) startAutoDetection()
})

onUnmounted(() => stopCamera())
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.image-uploader { width: 100%; }
:deep(.el-upload-dragger) { width: 100%; height: 250px; }
.camera-box { width: 100%; }
.preview-video { width: 100%; height: 300px; object-fit: cover; border-radius: 8px; background: #000; }
</style>