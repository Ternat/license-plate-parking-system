import request from './request'

/**
 * User login API
 * @param {Object} data - Login credentials { username, password }
 * @returns {Promise} Login response with token
 */
export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  }).then(res => {
    if (res.code === 200 && res.data?.access_token) {
      localStorage.setItem('token', res.data.access_token)
    }
    return res
  })
}

/**
 * User logout API
 * @returns {Promise} Logout response
 */
export function logout() {
  return request({
    url: '/auth/logout',
    method: 'post'
  }).then(() => {
    localStorage.removeItem('token')
  })
}