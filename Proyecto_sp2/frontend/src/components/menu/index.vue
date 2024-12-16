<template>
  <v-container>
    <!-- Carousel for promotional menus -->
    <v-row v-if="getDescript" class="my-4 d-flex justify-center">
      <v-col cols="12" md="8" offset="2">
        <div class="container">
          <div class="box">
      <p class="font-italic">
        "{{ getDescript }}"
      </p>
      
    </div>
          </div>
      </v-col>
     </v-row>
    <v-row class="mt-5 d-flex justify-center">
      <h2 class="promo-title">Nuestro Menú </h2>
    </v-row>
    <v-row class="mt-5 d-flex justify-center">
      <v-col cols="12" md="3"  v-for="category in categories" :key="category.name" class="category-container">
        <div class="container">
          <div class="box">
            <div class="top-bar"></div>
            <div class="content">
              <a :href="'/categoria/' + category.id">
                <v-img :src="category.image" class="category-image"></v-img>
                <strong class="category-title">{{ category.name }}</strong>
              </a>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>

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
      <v-row class="mt-5 d-flex justify-center">
        <v-col cols="12" md="4" offset="4" class="category-container">
          <v-btn href="/promos">
          Mira nuestras promociones
          <v-icon icon="mdi-location-enter"></v-icon>
        </v-btn>
        </v-col>
      </v-row>
    </template>
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
  computed: {
    getDescript() {
      return localStorage.getItem('DescriptionRest');
    }
  }
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

*{
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

body{
  width: 100%;
  font-family: 'Roboto', sans-serif;
  margin: 0;
  padding: 0;
  background: #b8dae3;
  display: flex;
  justify-content: center;
  flex-direction: column;
}
a{
  text-decoration: none;
}


.h1-text{
  font-size: 1.3rem;
  margin: 40px 0;
  color: #2c2c2c;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.h1-text i{
  background-color: #509bfc;
  color: #fff;
  width: 40px;
  height: 40px;
  box-shadow: 2px 5px 30px rgba(80, 123, 252, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
  margin: 0 20px;
}

.container{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
} 


.box{
  position: relative;
  min-width: 250px;
  background-color: #fff;
  box-shadow: 2px 3px 30px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin: 20px;
  position: relative;
  border-radius: 10px;
}


.top-bar{
  width: 50%;
  height: 4px;
  background: #507bfc;
  position: absolute;
  top: 0px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 0px 0px 10px 10px;
}

.top{
  display: flex;
  justify-content: space-between;
  align-items:center ;
  width: 100%;
}

.fa-check-circle{
  color: #17b667;
}

/* creating heart */
.heart{
  color: rgba(155,155,155);
}
.heart::before{
  content: '\f004';
  font-family: fontawesome;
  line-height: 30px;
  cursor: pointer;
  z-index: 1;
  transition: all 0.3s;
}
.box .heart-btn:checked ~ .heart::before{
  color:#e41934
}
.heart-btn{
  position: absolute;
  top: 25px;
  right: 20px;
  padding: 1rem;
  display: none;
}


.content img{
  width: 90px;
  height: 90px;
  border-radius:100px;
  overflow: hidden;
  object-fit: cover;
  object-position: top;
}
.content{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.content strong{
  font-weight: 500;
  color: #141414;
  margin-top: 10px;
}
.content p{
  font-size: 0.9rem;
  color: #7a7a7a;
  margin: 4px 0px 10px 0px;
  cursor: pointer;
}
.content p:hover{
  text-decoration: underline;
}

.category-image {
border-radius: 50%;
object-fit: cover;
}
</style>
