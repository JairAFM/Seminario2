import { createRouter, createWebHistory } from 'vue-router';
import ReservationPlane from '../components/ReservationPlane.vue'; 
import ReservationForm from '../components/ReservationForm.vue'; 
import FotoForm from '../components/PanoramaViewer.vue'; 
import ReservationDetails from '../components/ReservationDetails.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: ReservationPlane, // Muestra ReservationPlane en la raíz
  },
  {
    path: '/reserve',
    name: 'Reserve',
    component: ReservationForm, // Asegúrate de que esta ruta tenga el componente correcto
  },
  {
    path: '/fotos',
    name: 'Foto',
    component: FotoForm, // Asegúrate de que esta ruta tenga el componente correcto
  },
  {
    path: '/reservation-details/:id', // Usar :id para capturar el ID en la ruta
      component: ReservationDetails,
      name: 'reservation-details',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
