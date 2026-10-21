<template>
  <el-card shadow="hover">
    <template #header>
      <div class="card-header">
        <span style="font-size: 18px; font-weight: bold">End-to-End License Plate Recognition</span>
      </div>
    </template>
    <el-row :gutter="30">
      <el-col :span="12">
        <el-upload
          class="image-uploader"
          drag
          :auto-upload="false"
          :on-change="handleFileChange"
          :show-file-list="false"
          accept="image/*"
        >
          <el-icon class="el-icon--upload" style="font-size: 60px; color: #409eff"><UploadFilled /></el-icon>
          <div class="el-upload__text" style="margin-top: 15px; font-size: 16px">
            Drag vehicle image here or <em style="color: #409eff">click to upload</em>
          </div>
          <template #tip>
            <div class="el-upload__tip" style="margin-top: 10px; color: #999">
              Supported formats: JPG/PNG | Recommended: Clear image with visible license plate
            </div>
          </template>
        </el-upload>
        <div v-if="previewImage" style="margin-top: 25px; text-align: center">
          <el-image 
            :src="previewImage" 
            style="width: 100%; max-height: 450px; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1)" 
            fit="contain" 
            :preview-src-list="[previewImage]"
          />
        </div>
      </el-col>
      <el-col :span="12">
        <el-button 
          type="primary" 
          size="large" 
          @click="startRecognition" 
          :loading="isLoading"
          style="width: 100%; margin-bottom: 25px; height: 50px; font-size: 16px"
        >
          <el-icon><VideoPlay /></el-icon>
          Start Recognition
        </el-button>

        <el-descriptions 
          v-if="recognitionResult" 
          title="Recognition Result" 
          :column="1" 
          border
          style="background-color: white"
        >
          <el-descriptions-item label="Plate Number" label-style="width: 150px; font-weight: bold">
            <span style="font-size: 24px; font-weight: bold; color: #409eff">{{ recognitionResult.plate_number }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="Total Confidence">
            <el-tag type="success" size="large">{{ recognitionResult.total_confidence }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Detection Confidence">
            {{ recognitionResult.detect_confidence }}
          </el-descriptions-item>
          <el-descriptions-item label="OCR Confidence">
            {{ recognitionResult.ocr_confidence }}
          </el-descriptions-item>
        </el-descriptions>

        <el-empty v-else-if="!previewImage" description="Please upload a vehicle image first" />
      </el-col>
    </el-row>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { recognizeLicensePlate } from '@/api/recognition'

const previewImage = ref('')
const selectedFile = ref(null)
const isLoading = ref(false)
const recognitionResult = ref(null)

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  previewImage.value = URL.createObjectURL(file.raw)
  recognitionResult.value = null
}

const startRecognition = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('Please upload a vehicle image first!')
    return
  }

  isLoading.value = true
  try {
    const response = await recognizeLicensePlate(selectedFile.value)
    recognitionResult.value = response.data
    ElMessage.success('Recognition completed successfully!')
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.image-uploader {
  width: 100%;
}
:deep(.el-upload-dragger) {
  width: 100%;
  height: 250px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>