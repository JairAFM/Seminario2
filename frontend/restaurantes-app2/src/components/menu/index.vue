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
      <v-col cols="12" md="4" offset="4">
        <v-btn>
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
export default {
  data() {
    return {
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
      categories: [
        {
          name: "Desayunos",
          image: "https://www.comedera.com/wp-content/uploads/2022/12/Desayono-americano-shutterstock_2120331371.jpg",
        },
        {
          name: "Almuerzos y cenas",
          image: "https://th.bing.com/th/id/R.6d78a5abe7fc07afd91fffb7f8d45c93?rik=4s1asuo2b6Qt2Q&riu=http%3a%2f%2fwww.protocolo.org%2fextfiles%2fi-99-cG.16432.1.jpg&ehk=IWVhbkxAVSun6lZdXV0uz%2fwd4mgAT2fQ40tiX7nsbNY%3d&risl=&pid=ImgRaw&r=0",
        },
        {
          name: "Postres",
          image: "https://th.bing.com/th/id/R.f4cd8cd2f8cd977be6e63c63bd00e837?rik=foO9yc8oPxpxpg&riu=http%3a%2f%2fpostresrapidos.net%2fwp-content%2fuploads%2f2014%2f06%2fconsejos-para-preparar-postres.jpg&ehk=KmWFV2kr3AhKz4KvAQgTSXtqRm42ZrPxtyG0LNQIiZU%3d&risl=&pid=ImgRaw&r=0",
        },
        {
          name: "Café",
          image: "https://th.bing.com/th/id/R.6d30aa3368cbf1fe2b11cce8d7019990?rik=CvBk%2fI3KQ4IXqA&riu=http%3a%2f%2f4.bp.blogspot.com%2f-gwVTVpaWHf8%2fUTFWJeZ9kTI%2fAAAAAAABr9U%2fyBAwDuAjF5E%2fs1600%2ffotos-e-im%C3%A1genes-de-granos-de-caf%C3%A9-y-taza-coffee-photos-5.jpg&ehk=iHJ5c6jZ5EQ0H2yTf5UNn7HDV6GmXIAsz9MawudWEcU%3d&risl=&pid=ImgRaw&r=0",
        },
        {
          name: "Bebidas",
          image: "https://www.ella.sv/__export/1532376721450/sites/prensagrafica/img/2018/07/23/tres_bebidas_de_temporada.jpg_1015297233.jpg",
        },
        {
          name: "Antojos",
          image: "https://th.bing.com/th/id/R.089281aad9e4eb35d0a58c5ddb3de125?rik=3XQictzoR%2bLR1Q&riu=http%3a%2f%2fcdn.kiwilimon.com%2fclasificacion%2f2002%2f2002.jpg&ehk=knvDK9RPPvB18E1J6Mv3dTTpoZETTL0VLBx%2bttu9BQU%3d&risl=&pid=ImgRaw&r=0",
        }
      ],
    };
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
