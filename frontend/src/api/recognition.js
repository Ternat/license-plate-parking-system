import request from './request'

export function recognizeLicensePlate(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/recognition/run',
    method: 'post',
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}