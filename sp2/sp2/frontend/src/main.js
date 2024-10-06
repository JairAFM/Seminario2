import { createApp } from 'vue';
import App from './App.vue';
import router from './router/router.js'; // Asegúrate de importar el enrutador

const app = createApp(App);
app.use(router);  // Cargar el enrutador
app.mount('#app');
