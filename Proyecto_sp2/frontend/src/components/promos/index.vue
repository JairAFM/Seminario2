<template>
    <v-app>
      <!-- Barra lateral con categorías de comida -->
  
      <!-- Encabezado -->
      <v-app-bar app color="red darken-2" dark>
        <v-app-bar-title>Promociones de Comida</v-app-bar-title>
      </v-app-bar>
  
      <!-- Contenido principal con las promociones -->
      <v-main>
        <v-container fluid>
        <v-list lines="one" v-if="false">
          <v-list-group active-class="v-item--active">
            <template v-for="category in categories" :key="category.Id">
              <v-list-item @click="filterPromotions(category.id)">
                  <v-list-item-title>{{ category.description }}</v-list-item-title>
              </v-list-item>
            </template>
          </v-list-group>
        </v-list>
          <v-row class="mt-5 d-flex justify-center" v-if="verPromos">
                <v-col cols="12" md="3" v-for="formMenu in promotionalMenus" :key="formMenu.Id">
                    <v-card>
                    <v-carousel
                        height="200"
                        show-arrows="hover"
                        cycle
                        hide-delimiter-background
                    >
                        <template
                        v-for="(slide, i) in formMenu.Imagenes"
                        :key="i"
                        >
                        <v-carousel-item
                            :src="baseUrl + 'upload_menu/' + slide"
                            cover
                        ></v-carousel-item>
                        </template>
                    </v-carousel>
                    <v-card-text>
                        <h3>{{ formMenu.Titulo }}</h3>
                        <p class="d-inline-block text-truncate" style="max-width: 100%;">{{ formMenu.Descripcion }}</p>
                        <p :class="formMenu.promo ? 'text-decoration-line-through' : ''"><strong>Precio: </strong>{{formatCurrency(formMenu.Precio)}}</p>
                        <div v-if="formMenu.promo">
                        <h4>Promocion especial</h4>
                        <p>Del <strong>{{ formatDate(formMenu.inicio_promo) }}</strong> al <strong>{{ formatDate(formMenu.fin_promo) }}</strong></p>
                        <p><strong>Precio: </strong>{{formatCurrency(formMenu.precio_promo)}}</p>
                        </div>
                    </v-card-text>
                    <v-card-actions>
                    <v-btn color="yellow darken-4">
                        ¡Ordenar Ahora!
                        <v-icon right>mdi-cart</v-icon>
                    </v-btn>
                    </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
            <v-row class="mt-5 d-flex justify-center" v-else>
            <h2 class="promo-title">No tenemos promociones disponibles por el momento</h2>
        </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        baseUrl: 'http://127.0.0.1:5000/',
        drawer: false,
        selectedCategory: 'Todas',
        promotionalMenus: [],
        filteredPromotions: [],
        categories: [],
        verPromos: false,
      };
    },
    mounted() {
      this.getPromos();// Mostrar todas las promociones inicialmente
      this.getCategories();
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
      // Filtrar promociones según la categoría seleccionada
      filterPromotions(category) {
        if (category === 'Todas') {
          this.filteredPromotions = this.promotionalMenus;
        } else {
          this.filteredPromotions = this.promotions.filter(promotion => promotion.category === category);
        }
      },
      // Función para agregar el producto al carrito
      addToCart(promotion) {
        alert(`${promotion.title} agregado al carrito.`);
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
          this.categories = json;
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
          this.filteredPromotions = this.promotionalMenus; 
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
  .v-application {
    background-color: #f5f5f5;
  }
  
  .v-list-item--active {
    background-color: #ffcc00 !important;
  }
  </style>
  