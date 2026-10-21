<template>
  <el-card shadow="hover">
    <template #header>
      <div class="card-header">
        <span style="font-size: 18px; font-weight: bold">Vehicle Exit</span>
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
          <video ref="videoRef" autoplay muted playsinline class="preview-video"></video>
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
            <el-icon style="font-size: 60px; color: #f56c6c"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              Drag image here or click to upload
            </div>
          </el-upload>
        </div>

        <div v-if="previewImage" style="margin-top:20px;text-align:center">
          <el-image :src="previewImage" style="width:100%;max-height:300px;border-radius:8px" fit="contain" />
        </div>
      </el-col>

      <el-col :span="12">
        <el-button
          v-if="!autoMode"
          type="danger"
          size="large"
          @click="handleExit"
          :loading="isLoading"
          style="width:100%;height:50px"
        >
          <el-icon><CircleClose /></el-icon>
          Confirm Exit
        </el-button>

        <el-result v-if="exitResult" icon="success" title="Vehicle Exit Successful">
          <template #sub-title>
            <el-descriptions :column="1" :border="true" :style="{backgroundColor:'white'}">
              <el-descriptions-item label="Plate">{{ exitResult.plate_number }}</el-descriptions-item>
              <el-descriptions-item label="Fee">£{{ exitResult.parking_fee }}</el-descriptions-item>
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
import { vehicleExit } from '@/api/parking'
import { UploadFilled, CircleClose } from '@element-plus/icons-vue'

const previewImage = ref('')
const selectedFile = ref(null)
const isLoading = ref(false)
const exitResult = ref(null)
const autoMode = ref(false)

const videoRef = ref(null)
let stream = null
let timer = null
let lastCall = 0
const cooldown = 8000

const resetAll = () => {
  previewImage.value = ''
  selectedFile.value = null
  exitResult.value = null
  stopCamera()
}

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  previewImage.value = URL.createObjectURL(file.raw)
  exitResult.value = null
}

const handleExit = async () => {
  if (!selectedFile.value) return
  isLoading.value = true
  try {
    const res = await vehicleExit(selectedFile.value)
    exitResult.value = res.data
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
        vehicleExit(file).then(res => {
          exitResult.value = res.data
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