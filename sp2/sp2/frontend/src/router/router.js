import { createRouter, createWebHistory } from 'vue-router';
import ReservationPlane from '../components/ReservationPlane.vue'; 
import ReservationForm from '../components/ReservationForm.vue'; 
import FotoForm from '../components/PanoramaViewer.vue'; 
import ReservationDetails from '../components/ReservationDetails.vue';
import DescripcionPlatillo from '../components/DescripcionPlatillo.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: ReservationPlane, 
  },
  {
    path: '/reserve',
    name: 'Reserve',
    component: ReservationForm, 
  },
  {
    path: '/fotos',
    name: 'Foto',
    component: FotoForm,
  },
  {
    path: '/reservation-details/:id', 
      component: ReservationDetails,
      name: 'reservation-details',
  },
  {
    path: '/descripcion',
      component: DescripcionPlatillo,
      name: 'descripcion-platillo',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
