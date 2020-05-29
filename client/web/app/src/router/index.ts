import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [  
  {
    path: '/',
    name: 'root',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Root.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
  },
  {
    path: '/requests',
    name: 'requests',
    component: () => import('@/views/Request.vue')
  },
  {
    path: '/management',
    name: 'management',
    component: () => import('@/views/Management.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
