<template>
  <div class="image-upload-wrapper">
    <div
      class="upload-area"
      :class="{ 'is-dragover': isDragover }"
      @click="triggerFileInput"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragover = true"
      @dragleave.prevent="isDragover = false"
    >
      <input
        ref="fileInputRef"
        type="file"
        :accept="acceptedFileTypes"
        style="display: none"
        @change="handleFileSelect"
      />
      
      <div v-if="previewUrl" class="preview-container">
        <img :src="previewUrl" alt="Preview" class="preview-image" />
        <el-button type="danger" size="small" circle @click.stop="clearImage" class="clear-btn">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      
      <div v-else class="empty-state">
        <el-icon :size="48" color="#909399"><Upload /></el-icon>
        <p class="upload-text">Click or drag image here to upload</p>
        <p class="upload-hint">Supports {{ acceptedFileTypes }}, max {{ maxFileSizeMB }}MB</p>
      </div>
    </div>

    <el-progress
      v-if="uploading"
      :percentage="uploadProgress"
      :stroke-width="8"
      style="margin-top: 16px"
    />

    <el-alert
      v-if="errorMessage"
      type="error"
      :closable="true"
      style="margin-top: 16px"
      @close="errorMessage = ''"
    >
      {{ errorMessage }}
    </el-alert>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Upload, Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import request from '@/api/request' 

const props = defineProps({
  acceptedFileTypes: {
    type: String,
    default: '.jpg,.jpeg,.png'
  },
  maxFileSizeMB: {
    type: Number,
    default: 10
  },
  uploadUrl: {
    type: String,
    default: '/api/v1/recognition/upload'
  }
})

const emit = defineEmits(['upload-success', 'upload-error', 'clear'])
const fileInputRef = ref(null)
const isDragover = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const previewUrl = ref('')
const selectedFile = ref(null)
const errorMessage = ref('')
const maxFileSizeBytes = computed(() => props.maxFileSizeMB * 1024 * 1024)
const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const validateFile = (file) => {
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
  const allowedTypes = props.acceptedFileTypes.split(',')
  if (!allowedTypes.includes(fileExtension)) {
    errorMessage.value = `Unsupported file type: ${fileExtension}. Please upload ${props.acceptedFileTypes}.`
    return false
  }
  if (file.size > maxFileSizeBytes.value) {
    errorMessage.value = `File too large: ${(file.size / 1024 / 1024).toFixed(2)}MB. Maximum allowed: ${props.maxFileSizeMB}MB.`
    return false
  }
  errorMessage.value = ''
  return true
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) processFile(file)
  event.target.value = ''
}

const handleDrop = (event) => {
  isDragover.value = false
  const file = event.dataTransfer.files[0]
  if (file) processFile(file)
}

const processFile = (file) => {
  if (!validateFile(file)) return

  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
  emit('clear')
}

const clearImage = () => {
  previewUrl.value = ''
  selectedFile.value = null
  errorMessage.value = ''
  uploadProgress.value = 0
  emit('clear')
}

const uploadImage = async () => {
  if (!selectedFile.value) {
    errorMessage.value = 'chose a picture'
    return null
  }

  uploading.value = true
  uploadProgress.value = 0
  errorMessage.value = ''

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await request({
      url: props.uploadUrl,
      method: 'POST',
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
      }
    })

    ElMessage.success('success')
    emit('upload-success', response.data)
    return response.data
  } catch (error) {
    const errMsg = error.response?.data?.detail || error.message || 'fail'
    errorMessage.value = errMsg
    emit('upload-error', error)
    ElMessage.error(errMsg)
    return null
  } finally {
    uploading.value = false
  }
}

defineExpose({ uploadImage, clearImage })
</script>

<style scoped>
.image-upload-wrapper {
  width: 100%;
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  background-color: #fafafa;
}

.upload-area:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.upload-area.is-dragover {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.empty-state .upload-text {
  margin: 16px 0 8px;
  font-size: 16px;
  color: #606266;
}

.empty-state .upload-hint {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.preview-container {
  position: relative;
  display: inline-block;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.clear-btn {
  position: absolute;
  top: -10px;
  right: -10px;
}
</style>