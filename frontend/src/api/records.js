import request from './request'

export function getAllRecords(skip = 0, limit = 100) {
  return request({
    url: '/records/all',
    method: 'get',
    params: { skip, limit }
  })
}

export function getRecordsByPlate(plateNumber) {
  return request({
    url: '/records/by-plate',
    method: 'get',
    params: { plate_number: plateNumber }
  })
}

export function getActiveRecords() {
  return request({
    url: '/records/active',
    method: 'get'
  })
}