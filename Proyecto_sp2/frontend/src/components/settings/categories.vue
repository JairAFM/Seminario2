<template>
    <v-container>
      <v-card>
        <v-card-title>
          Mantenimiento de Categorías
          <v-spacer></v-spacer>
          <v-btn @click="openDialog('add')" color="primary" append-icon="mdi-plus">Agregar</v-btn>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="categories"
          item-value="id"
          class="elevation-1"
          items-per-page-text="Registros por página"
          no-data-text="No se han encontrado datos disponibles"
          :items-per-page-options="[{value: 10, title: '10'},
                                    {value: 20, title: '20'},
                                    {value: 30, title: '30'}]"
        >
          <template v-slot:[`item.actions`]="{ item }">
            <v-btn icon @click="openDialog('edit', item)" class="mx-2">
              <v-icon color="green">mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteCategory(item.id)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span v-if="dialogType === 'add'">Agregar Categoría</span>
            <span v-else>Editar Categoría</span>
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="form.description"
              label="Descripción"
              required
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" text @click="closeDialog">Cancelar</v-btn>
            <v-btn color="blue darken-1" text @click="saveCategory">Guardar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import Swal from 'sweetalert2'
  
  export default {
  data() {
    return {
      baseUrl: 'http://127.0.0.1:5000/',
      headers: [
        { title: 'ID', key: 'id' },
        { title: 'Descripción', key: 'description' },
        { title: 'Acciones', align: 'center', key: 'actions', sortable: false },
      ],
      categories: [],
      dialog: false,
      dialogType: 'add',
      form: {
        id: null,
        description: '',
      },
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
    openDialog(type, item = null) {
      this.dialogType = type;
      if (type === 'edit' && item) {
        this.form = { ...item };
      } else {
        this.form = { id: null, description: '' };
      }
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    async saveCategory() {
      if (this.dialogType === 'add') {
        if (!this.form.description) {
          Swal.fire({
            title: '¡Advertencia!',
            text: 'La descripción no puede ser nula',
            icon: 'warning'
          });
          return null;
        }
        const url = this.baseUrl + "newCategoria";
        const request1 = new Request(url, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json' // Ensure you're sending JSON
          },
          body: JSON.stringify({ description: this.form.description }),
        })
        const response1 = await fetch(request1);
        if (response1.status == 200) {
          Swal.fire({
            title: '¡Categoría Creada!',
            text: 'Se ha creado una nueva categoría exitosamente',
            icon: 'success'
          });
          this.getCategories();
        } else {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al crear la categoría, comuníquese con su proveedor correspondiente',
            icon: 'warning'
          });
        }
      } else if (this.dialogType === 'edit') {
        if (!this.form.description) {
          Swal.fire({
            title: '¡Advertencia!',
            text: 'La descripción no puede ser nula',
            icon: 'warning'
          });
          return null;
        }
        const index = this.categories.findIndex(c => c.id === this.form.id);
        if (index === -1) {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Los datos no coinciden, por favor recargue la página',
            icon: 'error'
          });
          this.closeDialog();
          return null;
        }
        const url = this.baseUrl + "editCategoria";
        fetch(url + '/' + this.form.id, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            description: this.form.description
          })
        })
        .then(response => {
          if (!response.ok) {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar actualizar los datos',
              icon: 'error'
            });
            return null;
          }
          Swal.fire({
            title: '¡Datos Actualizados!',
            text: 'Datos actualizados exitosamente',
            icon: 'success'
          });
          this.getCategories();
        })
        .catch(error => {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al intentar actualizar los datos',
              icon: 'error'
            });
            return null;
        });
      }
      this.closeDialog();
    },
    async deleteCategory(id) {
      try {
        const url = `${this.baseUrl}deleteCategoria/${id}`;
        
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
  
        if (response.ok) {
          Swal.fire({
            title: '¡Categoría Eliminada!',
            text: 'La categoría ha sido eliminada exitosamente',
            icon: 'success'
          });
          this.getCategories();
        } else if (response.status === 404) {
          Swal.fire({
            title: '¡Categoría No Encontrada!',
            text: 'No se encontró la categoría que desea eliminar.',
            icon: 'warning'
          });
        } else {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al eliminar la categoría. Comuníquese con su proveedor correspondiente.',
            icon: 'warning'
          });
        }
      } catch (error) {
        Swal.fire({
          title: '¡Ha ocurrido un error!',
          text: 'Ocurrió un error al eliminar la categoría. Comuníquese con su proveedor correspondiente.',
          icon: 'warning'
        });
      }
    },
  },
  };
  </script>
  
  <style scoped>
  .elevation-1 {
  margin-top: 20px;
  }
  </style>