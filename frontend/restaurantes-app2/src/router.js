import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from './components/HelloWorld.vue'
import Maintenances from './components/settings/index.vue'
import Categories from './components/settings/categories.vue'
import Status from './components/settings/status.vue'

const routes = [
    { 
        path: '/', 
        name: 'Inicio',
        component: HomeView 
    },
    { 
        path: '/maintenances', 
        name: 'Mantenimientos',
        component: Maintenances
    },
    {
        path: '/maintenances/categories',
        name: 'Categorias',
        component: Categories,
    },
    {
        path: '/maintenances/status',
        name: 'Estados',
        component: Status,
    }
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router