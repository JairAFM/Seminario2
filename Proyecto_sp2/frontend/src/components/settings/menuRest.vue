<template>
    <v-container>
      <v-row>
        <v-col>
          <v-btn color="primary" v-show="!showNewMenu" @click="showNewMenu = true">Nuevo Menu</v-btn>
          <v-btn color="error" v-show="showNewMenu" @click="limpiar">Cancelar</v-btn>
        </v-col>
      </v-row>
      <div v-show="showNewMenu">
        <!-- Formulario de Ingreso de Platillo -->
        <v-card>
          <v-card-title>Agregar Nuevo Platillo</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="formData.Titulo"
                label="Título"
                required
              ></v-text-field>
              <v-textarea
                v-model="formData.Descripcion"
                label="Descripción"
                required
              ></v-textarea>
              <v-text-field
                v-model="formData.Precio"
                label="Precio"
                type="number"
                required
              ></v-text-field>
              <v-combobox
                clearable
                label="Categoria"
                item-title="description"
                item-value="id"
                v-model="formData.Id_Categoria"
                :items="categorias"
              ></v-combobox>
              <v-file-input
                @change="onFileChange"
                label="Imagen del platillo"
                accept="image/*"
                prepend-icon="mdi-camera"
                chips
                multiple
                required
              ></v-file-input>
              <v-checkbox
                v-model="formData.promo"
                label="Promocion"
                :value="1"
              ></v-checkbox>
              <div v-show="formData.promo">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.inicio_promo"
                      type="date"
                      label="Inicio"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="formData.fin_promo"
                      type="date"
                      label="Fin"
                      :rules="[verifyfechaPromo]"
                    ></v-text-field>
                  </v-col>
                </v-row>
                <v-text-field
                  v-model="formData.precio_promo"
                  label="Precio"
                  type="number"
                  :rules="[verifyPrecioPromo]"
                ></v-text-field>
              </div>
            </v-form>
            <!-- Botón para Vista Previa -->
            <v-btn @click="showPreview = true" :disabled="blockPreview">Vista Previa</v-btn>
            <template v-if="imagesEdit">
                <h2>Imagenes Actuales</h2>
                <v-carousel
                  max-height="200"
                  
                  show-arrows="hover"
                  cycle
                  hide-delimiter-background
                >
                  <template
                    v-for="(img, i) in imagesEdit"
                    :key="i"
                  >
                    <v-carousel-item
                      :src="baseUrl + 'upload_menu/' + img"
                      cover
                    ></v-carousel-item>
                  </template>
                </v-carousel>
            </template>
          </v-card-text>
          <v-card-actions>
            <v-btn v-if="!showEditDialog" color="blue darken-1" text @click="submitForm" :disabled="!valid">Agregar Platillo</v-btn>
            <v-btn v-else color="blue darken-1" text @click="updateMenuItem" :disabled="!valid">Editar Platillo</v-btn>
          </v-card-actions>
        </v-card>
  
        <!-- Vista Previa del Platillo -->
        <v-dialog 
          v-model="showPreview" 
          max-width="500px"
          color="amber-lighten-3"
        >
          <v-card>
            <v-card-title>Vista Previa del Platillo</v-card-title>
            <v-carousel
              height="200"
              show-arrows="hover"
              cycle
              hide-delimiter-background
            >
              <template
                v-for="(slide, i) in formData.image"
                :key="i"
              >
                <v-carousel-item
                  :src="slide.temporal"
                  cover
                ></v-carousel-item>
              </template>
            </v-carousel>
            <v-card-text>
              <h3>{{ formData.Titulo }}</h3>
              <p class="d-inline-block text-truncate" style="max-width: 100%;">{{ formData.Descripcion }}</p>
              <p :class="formData.promo ? 'text-decoration-line-through' : ''"><strong>Precio: </strong>{{formatCurrency(formData.Precio)}}</p>
              <div v-if="formData.promo">
                <h4>Promocion especial</h4>
                <p>Del <strong>{{ formatDate(formData.inicio_promo) }}</strong> al <strong>{{ formatDate(formData.fin_promo) }}</strong></p>
                <p><strong>Precio: </strong>{{formatCurrency(formData.precio_promo)}}</p>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="showPreview = false">Cerrar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
      <!-- Tabla para mostrar los platillos existentes -->
      <v-data-table :headers="headers" :items="menuItems" 
          item-value="id"
          class="elevation-1"
          items-per-page-text="Registros por página"
          no-data-text="No se han encontrado datos disponibles"
          :items-per-page-options="[{value: 10, title: '10'},
                                    {value: 20, title: '20'},
                                    {value: 30, title: '30'}]">
        <template v-slot:item.Promo="{ item }">
          <template v-if="item.Promo == 0">
            No
          </template>
          <template v-else>
            Si
          </template>
        </template>
        <template v-slot:item.FechaIni_Promo="{ item }">
          {{ formatDate(item.FechaIni_Promo) }}
        </template>
        <template v-slot:item.FechaFin_Promo="{ item }">
          {{ formatDate(item.FechaFin_Promo) }}
        </template>
        <template v-slot:item.acciones="{ item }">
          <v-btn icon class="mx-2" @click="openDialog('edit', item)"><v-icon color="green">mdi-pencil</v-icon></v-btn>
          <v-btn icon class="mx-2" @click="deleteMenuItem(item.Id)"><v-icon color="red">mdi-delete</v-icon></v-btn>
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script>
  import Swal from 'sweetalert2';
  
  export default {
    data() {
      return {
        baseUrl: 'http://127.0.0.1:5000/',
        formData: {
          id: null,
          Titulo: '',
          Descripcion: '',
          Precio: null,
          Id_Categoria: null,
          promo: 0,
          precio_promo: null,
          inicio_promo: null,
          fin_promo: null,
          image: []
        },
        editData: {},
        menuItems: [],
        categorias: [],
        headers: [
          { title: 'Id', key: 'Id' },
          { title: 'Título', key: 'Titulo' },
          { title: 'Descripción', key: 'Descripcion' },
          { title: 'Precio', key: 'Precio' },
          { title: 'Categoria', key: 'Categoria' },
          { title: 'Promocion', key: 'Promo' },
          { title: 'Precio Promo', key: 'Precio_Promo' },
          { title: 'Inicio Promo', key: 'FechaIni_Promo' },
          { title: 'Fin Promo', key: 'FechaFin_Promo' },
          { title: 'Acciones', key: 'acciones', sortable: false },
        ],
        valid: false,
        showPreview: false,
        showEditDialog: false,
        showNewMenu: false,
        blockPreview: false,
        imagesEdit: null,
      };
    },
    mounted() {
      this.getMenuItems();
      this.getCategories();
    },
    methods: {
      formatDate(dateString, formatField = false) {
        // Convertimos el string de la fecha a un objeto Date
        const date = new Date(dateString);
        
        // Extraemos el día, el mes y el año
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Los meses van de 0 a 11
        const year = date.getFullYear();
        
        if (formatField) {
          // Formateamos la fecha como dd/mm/yyyy
          return `${year}-${month}-${day}`;
        } else {
          // Formateamos la fecha como dd/mm/yyyy
          return `${day}/${month}/${year}`;
        }
      },
      verifyPrecioPromo() {
        if (this.formData.Precio < this.formData.precio_promo) {
          this.blockPreview = true;
          return 'El precio de la promocion debe ser menor al precio normal.';
        } else {
          this.blockPreview = false;
          return null;
        }
      },
      verifyfechaPromo() {
        if (this.formData.inicio_promo > this.formData.fin_promo) {
          this.blockPreview = true;
          return 'La fecha fin de promocion debe ser mayor a la fecha inicial.';
        } else {
          this.blockPreview = false;
          return null;
        }
      },
      formatCurrency(value) {
        return new Intl.NumberFormat('es-GT', {
          style: 'currency',
          currency: 'GTQ',
        }).format(value);
      },
      onFileChange(event) {
          const files = event.target.files;
          this.formData.image = [];
          for (let i = 0; i < files.length; i++) {
            const el = files[i];
            if (el) {
              const reader = new FileReader();
              reader.onloadend = () => {
                let data = {
                  name: el.name,
                  mimetype: el.type.split('/')[1],
                  image: reader.result.split(',')[1],
                  temporal: reader.result
                }
                this.formData.image.push(data);
              };
              reader.readAsDataURL(el);
            }
          }
        },
      async getMenuItems() {
        const url = this.baseUrl + 'menu';
        try {
          const response = await fetch(url);
          if (!response.ok) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar cargar los datos',
              icon: 'error',
            });
            return;
          }
          const json = await response.json();
          this.menuItems = json;
        } catch (error) {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al intentar cargar los datos',
            icon: 'error',
          });
        }
      },
      async submitForm() {
        if (!this.formData.Titulo || !this.formData.Descripcion || !this.formData.Precio || !this.formData.Id_Categoria) {
          Swal.fire({
            title: '¡Advertencia!',
            text: 'Todos los campos son requeridos',
            icon: 'warning',
          });
          return;
        }
        
        let data = {
          Titulo: this.formData.Titulo,
          Descripcion: this.formData.Descripcion,
          Precio: this.formData.Precio,
          Id_Categoria: this.formData.Id_Categoria.id,
          promo: this.formData.promo,
          precio_promo: this.formData.precio_promo,
          inicio_promo: this.formData.inicio_promo,
          fin_promo: this.formData.fin_promo,
          image: JSON.stringify(this.formData.image)
        };
        const url = this.baseUrl + 'menu';
        const request = new Request(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
  
        try {
          const response = await fetch(request);
          if (response.ok) {
            Swal.fire({
              title: '¡Platillo Agregado!',
              text: 'Se ha agregado un nuevo platillo exitosamente',
              icon: 'success',
            });
            this.limpiar();
            this.getMenuItems();
          } else {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al agregar el platillo',
              icon: 'error',
            });
          }
        } catch (error) {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al agregar el platillo',
            icon: 'error',
          });
        }
      },
      async updateMenuItem() {
        if (!this.formData.Titulo || !this.formData.Descripcion || !this.formData.Precio || !this.formData.Id_Categoria) {
          Swal.fire({
            title: '¡Advertencia!',
            text: 'Todos los campos son requeridos',
            icon: 'warning',
          });
          return;
        }
        
        let data = {
          Titulo: this.formData.Titulo,
          Descripcion: this.formData.Descripcion,
          Precio: this.formData.Precio,
          Id_Categoria: this.formData.Id_Categoria.id,
          promo: this.formData.promo,
          precio_promo: this.formData.precio_promo,
          inicio_promo: this.formData.inicio_promo,
          fin_promo: this.formData.fin_promo,
          image: JSON.stringify(this.formData.image)
        };
        const url = this.baseUrl + `menu/${this.formData.id}`;
        const request = new Request(url, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
  
        try {
          const response = await fetch(request);
          if (response.ok) {
            Swal.fire({
              title: '¡Platillo Actualizado!',
              text: 'El platillo ha sido actualizado exitosamente',
              icon: 'success',
            });
            this.limpiar();
            this.getMenuItems();
          } else {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al actualizar el platillo',
              icon: 'error',
            });
          }
        } catch (error) {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al actualizar el platillo',
            icon: 'error',
          });
        }
      },
      async deleteMenuItem(id) {
        const url = this.baseUrl + `menu/${id}`;
        const request = new Request(url, { method: 'DELETE' });
  
        try {
          const response = await fetch(request);
          if (response.ok) {
            Swal.fire({
              title: '¡Platillo Eliminado!',
              text: 'El platillo ha sido eliminado exitosamente',
              icon: 'success',
            });
            this.getMenuItems();
          } else {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al eliminar el platillo',
              icon: 'error',
            });
          }
        } catch (error) {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al eliminar el platillo',
            icon: 'error',
          });
        }
      },
      openDialog(type, item = null) {
        if (type === 'edit' && item) {
          console.log(item);
          this.formData =  {
            id: item.Id,
            Titulo: item.Titulo,
            Descripcion: item.Descripcion,
            Precio: item.Precio,
            Id_Categoria: item.Categoria,
            promo: item.Promo,
            precio_promo: item.Precio_Promo,
            inicio_promo: this.formatDate(item.FechaIni_Promo, true),
            fin_promo: this.formatDate(item.FechaFin_Promo, true),
            image: []
          }
          this.imagesEdit = JSON.parse(item.Imagenes);
          this.showEditDialog = true;
          this.showNewMenu = true;
        }
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
          this.categorias = json;
        } catch (error) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar cargar los datos',
              icon: 'error'
            });
            return null;
        }
      },
      limpiar() {
        this.formData = {
          id: null,
          Titulo: '',
          Descripcion: '',
          Precio: null,
          Id_Categoria: null,
          promo: 0,
          precio_promo: null,
          inicio_promo: null,
          fin_promo: null,
          image: []
        };
        this.showNewMenu = false;
        this.imagesEdit = null;
      }
    },
  };
  </script>
  
  <style scoped>
  .v-btn {
    margin: 10px;
  }
  </style>