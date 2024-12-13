<template>
    <div>
        <v-row class="mt-5 d-flex justify-center">
            <v-col cols="12" md="3"  v-for="category in categories" :key="category.name" class="category-container">
                <a :href="'/categoria/' + category.id">
                <v-img :src="category.image" class="category-image"></v-img>
                <p class="category-title">{{ category.name }}</p>
                </a>
            </v-col>
        </v-row>
        <template v-if="menu.length > 0">
            <v-row class="mt-5 d-flex justify-center">
                <h2 class="promo-title">Deleitate con nuestros deliciosos {{ titular[0].description }}</h2>
            </v-row>
            <v-row class="mt-5 d-flex justify-center">
                <v-col cols="12" md="3" v-for="formMenu in menu" :key="formMenu.Id">
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
                        <p :class="formMenu.Promo ? 'text-decoration-line-through' : ''"><strong>Precio: </strong>{{formatCurrency(formMenu.Precio)}}</p>
                        <div v-if="formMenu.Promo">
                        <h4>Promocion especial</h4>
                        <p>Del <strong>{{ formatDate(formMenu.FechaIni_Promo) }}</strong> al <strong>{{ formatDate(formMenu.FechaFin_Promo) }}</strong></p>
                        <p><strong>Precio: </strong>{{formatCurrency(formMenu.Precio_Promo)}}</p>
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
        </template>
        <v-row class="mt-5 d-flex justify-center" v-else>
            <h2 class="promo-title">No tenemos Menus disponibles por ahora, prueba a ver nuestras otras categorias</h2>
        </v-row>
    </div>
 </template>
<script>
import Swal from 'sweetalert2';
export default {
  data() {
    return {
      baseUrl: 'http://127.0.0.1:5000/',
      categories: [],
      id_categoria: null,
      menu: [],
      titular: null
    };
  },
  mounted() {
    this.id_categoria = this.$route.params.categoria;
    this.getCategories();
    this.getPlatillosCat();
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
            let json = await response.json();
            this.titular = json.filter(k => k.id == this.id_categoria);
            json = json.filter(k => k.id != this.id_categoria);
            json.forEach(e => {
            let data = {
                id: e.id,
                name: e.description,
                image: "https://th.bing.com/th/id/R.6d78a5abe7fc07afd91fffb7f8d45c93?rik=4s1asuo2b6Qt2Q&riu=http%3a%2f%2fwww.protocolo.org%2fextfiles%2fi-99-cG.16432.1.jpg&ehk=IWVhbkxAVSun6lZdXV0uz%2fwd4mgAT2fQ40tiX7nsbNY%3d&risl=&pid=ImgRaw&r=0",
            }
            this.categories.push(data);
            });
        } catch (error) {
            console.log(error);
            Swal.fire({
                title: '¡Ha ocurrido un error!',
                text: 'Ocurrió un error al intentar cargar los datos',
                icon: 'error'
            });
            return null;
        }
    },
    async getPlatillosCat() {
        const url = this.baseUrl + "getPlatillosCat/" + this.id_categoria;
        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.log(response);
                Swal.fire({
                    title: '¡Ha ocurrido un error!',
                    text: 'Ocurrió un error al intentar cargar el menu2',
                    icon: 'error'
                });
                return null;
            }
            let json = await response.json();
            json.forEach(el => {
                el.Imagenes = JSON.parse(el.Imagenes);
            });
            this.menu = json;
        } catch (error) {
            console.log(error);
            Swal.fire({
                title: '¡Ha ocurrido un error!',
                text: 'Ocurrió un error al intentar cargar el menu1',
                icon: 'error'
            });
            return null;
        }
    },
  },
};
</script>

<style scoped>
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

.promo-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: red;
}

</style>