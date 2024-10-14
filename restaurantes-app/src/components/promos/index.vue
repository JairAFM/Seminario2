<template>
    <v-app>
      <!-- Barra lateral con categorías de comida -->
      <v-navigation-drawer v-model="drawer" app>
        <v-list>
          <v-list-item-group v-model="selectedCategory" active-class="v-item--active">
            <v-list-item v-for="category in categories" :key="category">
              <v-list-item-content @click="filterPromotions(category)">
                <v-list-item-title>{{ category }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-navigation-drawer>
  
      <!-- Encabezado -->
      <v-app-bar app color="red darken-2" dark>
        <v-app-bar-title>Promociones de Comida</v-app-bar-title>
      </v-app-bar>
  
      <!-- Contenido principal con las promociones -->
      <v-main>
        <v-container fluid>
          <v-row>
            <v-col cols="12" md="4" v-for="promotion in filteredPromotions" :key="promotion.title">
              <v-card>
                <v-img :src="promotion.image" height="200px"></v-img>
                <v-card-title>{{ promotion.title }}</v-card-title>
                <v-card-subtitle>{{ promotion.description }}</v-card-subtitle>
                <v-card-actions>
                  <v-btn color="yellow darken-2" @click="addToCart(promotion)">
                    ¡Ordenar Ahora!
                    <v-icon right>mdi-cart</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        drawer: false,
        selectedCategory: 'Todas',
        categories: ['Todas', 'Desayunos', 'Almuerzos', 'Cenas', 'Postres', 'Bebidas'],
        promotions: [
  {
    title: "Combo de Desayuno",
    description: "Incluye café y tostadas por solo Q.10.00",
    image: "https://www.comedera.com/wp-content/uploads/2022/12/Desayono-americano-shutterstock_2120331371.jpg",
    category: "Desayunos",
  },
  {
    title: "Hamburguesa con Papas",
    description: "¡Llévate una hamburguesa doble con papas fritas por Q.15.00",
    image: "https://st2.depositphotos.com/1031681/5890/i/950/depositphotos_58908981-stock-photo-mini-hamburger-with-french-fries.jpg",
    category: "Almuerzos",
  },
  {
    title: "Combo Familiar de Cenas",
    description: "Cena para 4 personas a Q.20.00",
    image: "https://restaurantesganbei.com/wp-content/uploads/2023/01/combo-familiar.jpg",
    category: "Cenas",
  },
  {
    title: "Helado y Galleta",
    description: "Helado de vainilla con galleta por solo Q.05.00",
    image: "https://th.bing.com/th/id/OIP.8atoi9XbNfz1e37exonzSgHaE7?rs=1&pid=ImgDetMain",
    category: "Postres",
  },
  {
    title: "Batido de Fresa",
    description: "Delicioso batido de fresa por Q.07.50",
    image: "https://www.comedera.com/wp-content/uploads/2022/05/batido-de-fresa-y-cambur.jpg",
    category: "Bebidas",
  },
        ],
        filteredPromotions: [],
      };
    },
    mounted() {
      this.filteredPromotions = this.promotions; // Mostrar todas las promociones inicialmente
    },
    methods: {
      // Filtrar promociones según la categoría seleccionada
      filterPromotions(category) {
        if (category === 'Todas') {
          this.filteredPromotions = this.promotions;
        } else {
          this.filteredPromotions = this.promotions.filter(promotion => promotion.category === category);
        }
      },
      // Función para agregar el producto al carrito
      addToCart(promotion) {
        alert(`${promotion.title} agregado al carrito.`);
      },
    },
  };
  </script>
  
  <style scoped>
  .v-application {
    background-color: #f5f5f5;
  }
  
  .v-list-item--active {
    background-color: #ffcc00 !important;
  }
  </style>
  