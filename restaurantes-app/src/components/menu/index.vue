<template>
  <v-container>
    <!-- Carousel for promotional menus -->
    <v-carousel hide-delimiters height="400px" show-arrows>
      <v-carousel-item
        v-for="(promo, index) in promotionalMenus"
        :key="index"
        :src="promo.image"
      >
        <v-row align="center" justify="center" style="background-color: rgba(255, 255, 255, 0.8);">
          <v-col class="text-center">
            <h2 class="promo-title">{{ promo.title }}</h2>
            <p class="promo-subtitle">{{ promo.description }}</p>
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

    <!-- Menu category selection like the image -->
    <v-row class="mt-5">
      <v-col cols="12" md="4" v-for="category in categories" :key="category.name" class="category-container">
        <a href="#">
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
      promotionalMenus: [
        {
          title: "Hamburguesa especial",
          description: "Desde hoy hasta el 15 de septiembre en promocion",
          image: "https://newcoach2012.net/wp-content/uploads/2022/06/Hamburguesas.jpg",
        },
        {
          title: "Especial de carnes",
          description: "Prueba nuestro especial de carnes!",
          image: "https://th.bing.com/th/id/OIP.cUBfFrH7_fa0GLBpLcKmMAHaE8?rs=1&pid=ImgDetMain",
        },
        {
          title: "Papas fritas que te elevaran el apetito",
          description: "Prueba nuestra super promocion",
          image: "https://th.bing.com/th/id/OIP.f1R8kpo61Jk2qWFj3ruS3wAAAA?rs=1&pid=ImgDetMain",
        },
      ],
      // Menu categories with images
      categories: [],
    };
  },
  mounted() {
    this.getCategories();
  },
  methods: {
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
