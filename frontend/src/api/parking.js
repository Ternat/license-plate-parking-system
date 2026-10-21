import request from './request'

export function vehicleEntry(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/parking/entry',
    method: 'post',
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function vehicleExit(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/parking/exit',
    method: 'post',
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}