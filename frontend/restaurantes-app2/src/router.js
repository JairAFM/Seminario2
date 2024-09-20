import { createWebHistory, createRouter } from 'vue-router'

import HomeView from './components/menu/index.vue'
import Promos from './components/promos/index.vue'
import Maintenances from './components/settings/index.vue'
import Categories from './components/settings/categories.vue'
import positionEmployees from './components/settings/position-employees.vue'
import Status from './components/settings/status.vue'
import Employees from './components/settings/employees.vue'
import Tables from './components/settings/tables.vue'
import Menu from './components/settings/menu.vue'

const routes = [
    { 
        path: '/', 
        name: 'Inicio',
        component: HomeView 
    },
    { 
        path: '/promos', 
        name: 'Promociones',
        component: Promos 
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
        path: '/maintenances/positionEmployee',
        name: 'Puestos',
        component: positionEmployees,
    },
    {
        path: '/maintenances/status',
        name: 'Estados',
        component: Status,
    },
    {
        path: '/maintenances/employees',
        name: 'Empleados',
        component: Employees,
    },
    {
        path: '/maintenances/tables',
        name: 'Mesas',
        component: Tables,
    },
    {
        path: '/maintenances/menu',
        name: 'Menu',
        component: Menu,
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router