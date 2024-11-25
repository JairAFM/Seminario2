<template>
    <v-container>
      <!-- Carousel for promotional menus -->
       <template v-if="verPromos">
        <v-carousel hide-delimiters height="400px" show-arrows>
          <v-carousel-item
            v-for="(promo, index) in promotionalMenus"
            :key="index"
            :src="baseUrl + 'upload_menu/' + promo.Imagenes[0]"
          >
            <v-row align="center" justify="center" style="background-color: rgba(255, 255, 255, 0.8);">
              <v-col class="text-center">
                <h2 class="promo-title">{{ promo.Titulo }}</h2>
                <p class="promo-subtitle">Desde <strong>{{ formatDate(promo.FechaIni_Promo) }}</strong> hasta <strong>{{ formatDate(promo.FechaFin_Promo) }}</strong></p>
                <p class="promo-subtitle">A solo <strong>{{ formatCurrency(promo.Precio_Promo) }}</strong></p>
              </v-col>
            </v-row>
          </v-carousel-item>
        </v-carousel>
        <v-row class="mt-5">
          <v-col cols="12" md="4" offset="4" class="category-container">
            <v-btn href="/promos">
            Mira nuestras promociones
            <v-icon icon="mdi-location-enter"></v-icon>
          </v-btn>
          </v-col>
        </v-row>
      </template>
  
      <v-row class="mt-5 d-flex justify-center">
        <h2 class="promo-title">Deleitate con nuestros menus</h2>
      </v-row>
      <!-- Menu category selection like the image -->
      <v-row class="mt-5 d-flex justify-center">
        <v-col cols="12" md="3"  v-for="category in categories" :key="category.name" class="category-container">
          <a :href="'/categoria/' + category.id">
            <v-img :src="category.image" class="category-image"></v-img>
            <p class="category-title">{{ category.name }}</p>
          </a>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import Swal from 'sweetalert2';
  export default {
    data() {
      return {
        baseUrl: 'http://127.0.0.1:5000/',
        // Promotional carousel images and descriptions
        promotionalMenus: [],
        // Menu categories with images
        categories: [],
        verPromos: false,
      };
    },
    mounted() {
      this.getCategories();
      this.getPromos();
    },
    methods: {
      formatDate(dateString) {
        // Convertimos el string de la fecha a un objeto Date
        const date = new Date(dateString);
        
        // Extraemos el día, el mes y el año
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Los meses van de 0 a 11
        const year = date.getFullYear();
        
          // Formateamos la fecha como dd/mm/yyyy
          return `${day}/${month}/${year}`;
      },
      formatCurrency(value) {
        return new Intl.NumberFormat('es-GT', {
          style: 'currency',
          currency: 'GTQ',
        }).format(value);
      },
      async getCategories() {
        const url = this.baseUrl + "getCategories";
        try {
          const response = await fetch(url);
          if (!response.ok) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar cargar los datos',
              icon: 'error'
            });
            return null;
          }
          const json = await response.json();
          json.forEach(e => {
            let data = {
              id: e.id,
              name: e.description,
              image: "https://th.bing.com/th/id/R.6d78a5abe7fc07afd91fffb7f8d45c93?rik=4s1asuo2b6Qt2Q&riu=http%3a%2f%2fwww.protocolo.org%2fextfiles%2fi-99-cG.16432.1.jpg&ehk=IWVhbkxAVSun6lZdXV0uz%2fwd4mgAT2fQ40tiX7nsbNY%3d&risl=&pid=ImgRaw&r=0",
            }
            this.categories.push(data);
          });
        } catch (error) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar cargar los datos',
              icon: 'error'
            });
            return null;
        }
    },
    async getPromos() {
        const url = this.baseUrl + "getPromos";
        try {
          const response = await fetch(url);
          if (!response.ok) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar cargar los datos',
              icon: 'error'
            });
            return null;
          }
          const json = await response.json();
          json.forEach(el => {
            el.Imagenes = JSON.parse(el.Imagenes);
          });
          this.promotionalMenus = json;
          if (this.promotionalMenus.length > 0) {
            this.verPromos = true;
          }
        } catch (error) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar cargar los datos',
              icon: 'error'
            });
            return null;
        }
    },
    },
  };
  </script>
  
  <style scoped>
  /* Promotional carousel styling */
  .promo-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: red;
  }
  
  .promo-subtitle {
    font-size: 1.2rem;
    color: #333;
  }
  
  /* Category image and text styling */
  .category-container {
    text-align: center;
    padding: 20px;
  }
  
  .category-image {
    height: 150px;
    object-fit: contain;
  }
  
  .category-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: black;
    margin-top: 10px;
  }
  </style>