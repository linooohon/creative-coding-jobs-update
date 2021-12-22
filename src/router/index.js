import { createRouter, createWebHistory } from 'vue-router'
// import Dashboard from '../views/Dashboard.vue'
// import Keyword from '../views/Keyword.vue'
// import Search from '../views/Search.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/keyword',
    name: 'Keyword',
    component: () => import('../views/Keyword.vue')
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('../views/Search.vue')
  },
  {
    path: '/keyword/:targetKeyword',
    name: 'KeywordDashboard',
    component: () => import('../views/KeywordDashboard.vue'),
    props: true
  },
  {
    path: '/search',
    name: 'SearchDashboard',
    component: () => import('../views/SearchDashboard.vue'),
    props: (route) => route.params
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
