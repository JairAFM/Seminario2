import { createRouter, createWebHistory } from 'vue-router';
import ReservationPlane from '../components/ReservationPlane.vue'; 
import ReservationForm from '../components/ReservationForm.vue'; 
import FotoForm from '../components/PanoramaViewer.vue'; 
import ReservationDetails from '../components/ReservationDetails.vue';
import Interaccion from '../components/ChatdeDescripcion.vue';
import VistaPlatillo from '../components/VistaPlatillo.vue';
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
    path: '/descripcion',
    name: 'Descripcion',
    component: Interaccion, // Asegúrate de que esta ruta tenga el componente correcto
  },
  {
    path: '/reservation-details/:id', // Usar :id para capturar el ID en la ruta
      component: ReservationDetails,
      name: 'reservation-details',
  },
  {
    path: '/vistaplatillo', // Usar :id para capturar el ID en la ruta
      component: VistaPlatillo,
      name: 'vistaplatillo',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
