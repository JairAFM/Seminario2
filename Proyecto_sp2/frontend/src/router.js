import { createWebHistory, createRouter } from 'vue-router'

import CreateAccount from './components/session/create-account.vue'

import HomeView from './components/menu/index.vue'
import Promos from './components/promos/index.vue'
import Maintenances from './components/settings/index.vue'
import Categories from './components/settings/categories.vue'
import positionEmployees from './components/settings/position-employees.vue'
import Status from './components/settings/status.vue'
import Employees from './components/settings/employees.vue'
import Tables from './components/settings/tables.vue'
import Menu from './components/settings/menuRest.vue'
import menuCategory from './components/menu/categoriaComida.vue'
import DetallesReserva from './components/components_reserva/Detalles_reserva.vue'

import ReservationPlane from './components/components_reserva/ReservationPlane.vue'; 
import ReservationForm from './components/components_reserva/ReservationForm.vue'; 
import FotoForm from './components/components_reserva/PanoramaViewer.vue'; 
//import ReservationDetails from './components/components_reserva/ReservationDetails.vue';
//import DescripcionPlatillo from './components/components_reserva/DescripcionPlatillo.vue';

const routes = [
    { 
        path: '/', 
        name: 'Inicio',
        component: HomeView 
    },
    {
        path: '/crearCuenta', 
        name: 'Crear Cuenta',
        component: CreateAccount 
    },
    { 
        path: '/promos', 
        name: 'Promociones',
        component: Promos 
    },
    { 
        path: '/maintenances', 
        name: 'Mantenimientos',
        meta: { requiresAuth: true, requiresPermission: true },
        component: Maintenances
    },
    {
        path: '/maintenances/categories',
        name: 'Categorias',
        meta: { requiresAuth: true, requiresPermission: true },
        component: Categories,
    },
    {
        path: '/maintenances/positionEmployee',
        name: 'Puestos',
        meta: { requiresAuth: true },
        component: positionEmployees,
    },
    {
        path: '/maintenances/status',
        name: 'Estados',
        meta: { requiresAuth: true, requiresPermission: true },
        component: Status,
    },
    {
        path: '/maintenances/employees',
        name: 'Empleados',
        meta: { requiresAuth: true },
        component: Employees,
    },
    {
        path: '/maintenances/tables',
        name: 'Mesas',
        meta: { requiresAuth: true, requiresPermission: true },
        component: Tables,
    },
    {
        path: '/maintenances/menu',
        name: 'Menu',
        meta: { requiresAuth: true, requiresPermission: true },
        component: Menu,
    },
    {
        path: '/categoria/:categoria',
        name: 'nuestro Menu',
        component: menuCategory,
    },
    {
        path: '/reservation',
        name: 'Home',
        component: ReservationPlane, 
      },
    {
        path: '/resevarForm',
        name: 'Reserve',
        component: ReservationForm, 
      },
     {
        path: '/fotos',
        name: 'Foto',
        component: FotoForm,
      },
      {
        path: '/detallesReserva',
        name: 'DetalleReserva',
        component: DetallesReserva,
      },
      /*{
        path: '/reservation/reservation-details/:id', 
          component: ReservationDetails,
          name: 'reservation-details',
      },
      {
        path: '/reservation/descripcion',
          component: DescripcionPlatillo,
          name: 'descripcion-platillo',
      },*/
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Verificación global antes de acceder a rutas protegidas
router.beforeEach((to, from, next) => {
    document.title = 'FindTable - ' + to.name;
    const token = localStorage.getItem('token');  // Obtener el token almacenado
    const tipoUser = localStorage.getItem('tipoUser'); // Obtener tipo de usuario
  
    // Si la ruta requiere autenticación y no hay token, redirige al login
    if (to.matched.some(record => record.meta.requiresAuth) && !token) {
      next('/');
    } else if (to.matched.some(record => record.meta.requiresPermission) && tipoUser !== '0') {
      next('/');
    } else {
      next();  // Si hay token o la ruta no requiere autenticación, permite el acceso
    }
  });

export default router
