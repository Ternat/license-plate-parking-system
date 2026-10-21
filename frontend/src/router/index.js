import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout.vue'
import Recognition from '@/views/Recognition/Index.vue'
import Entry from '@/views/Parking/Entry.vue'
import Exit from '@/views/Parking/Exit.vue'
import Records from '@/views/Records/List.vue'
import Login from '@/views/Login.vue'

const routes = [
  
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: 'Login', requiresAuth: false }
  },
  
  {
    path: '/',
    component: Layout,
    redirect: '/recognition',
    meta: { requiresAuth: true },
    children: [
      { 
        path: 'recognition', 
        name: 'Recognition', 
        component: Recognition, 
        meta: { title: 'License Plate Recognition' } 
      },
      { 
        path: 'parking/entry', 
        name: 'Entry', 
        component: Entry, 
        meta: { title: 'Vehicle Entry' } 
      },
      { 
        path: 'parking/exit', 
        name: 'Exit', 
        component: Exit, 
        meta: { title: 'Vehicle Exit' } 
      },
      { 
        path: 'records', 
        name: 'Records', 
        component: Records, 
        meta: { title: 'Parking Records' } 
      },
      { 
        path: 'parking/price', 
        name: 'PriceManagement', 
        component: () => import('@/views/Parking/PriceManagement.vue'), 
        meta: { title: 'Price Management' } 
      }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'UK LPR Parking System'
  const requiresAuth = to.meta.requiresAuth
  const token = localStorage.getItem('token')

  if (requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/recognition')
  } else {
    next()
  }
})

export default router