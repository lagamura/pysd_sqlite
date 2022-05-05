import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import NewSimulation from '@/views/NewSimulation.vue'
import HistoryView from '@/views/HistoryView.vue'

const routes = [
    {
        path: '/',
        name: 'HomeView',
        component: HomeView
    },
    {
        path: '/new-simulation',
        name: 'NewSimulation',
        component: NewSimulation
    },
    {
        path: '/history',
        name: 'History',
        component: HistoryView
    },
    {
        path: '/about',
        name: 'AboutView',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
]
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})
export default router