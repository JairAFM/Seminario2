<template>
  <v-container>
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
          <v-select
            v-model="formData.Id_Categoria"
            :items="categorias"
            label="Categoría"
            required
          ></v-select>
        </v-form>
        <!-- Botón para Vista Previa -->
        <v-btn @click="showPreview = true">Vista Previa</v-btn>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="submitForm" :disabled="!valid">Agregar Platillo</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Vista Previa del Platillo -->
    <v-dialog v-model="showPreview" max-width="500px">
      <v-card>
        <v-card-title>Vista Previa del Platillo</v-card-title>
        <v-card-text>
          <h3>{{ formData.Titulo }}</h3>
          <p>{{ formData.Descripcion }}</p>
          <p><strong>Precio:</strong> ${{ formData.Precio }}</p>
          <p><strong>Categoría:</strong> {{ getCategoriaName(formData.Id_Categoria) }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="showPreview = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Tabla para mostrar los platillos existentes -->
    <v-data-table :items="menuItems" :headers="headers">
      <template v-slot:item.acciones="{ item }">
        <v-btn @click="openDialog('edit', item)">Editar</v-btn>
        <v-btn color="red" @click="deleteMenuItem(item.Id)">Eliminar</v-btn>
      </template>
    </v-data-table>

    <!-- Modal de edición -->
    <v-dialog v-model="showEditDialog" max-width="500px">
      <v-card>
        <v-card-title>Editar Platillo</v-card-title>
        <v-card-text>
          <v-form ref="editForm" v-model="valid">
            <v-text-field v-model="editData.Titulo" label="Título" required></v-text-field>
            <v-textarea v-model="editData.Descripcion" label="Descripción" required></v-textarea>
            <v-text-field v-model="editData.Precio" label="Precio" type="number" required></v-text-field>
            <v-select v-model="editData.Id_Categoria" :items="categorias" label="Categoría" required></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="updateMenuItem">Guardar</v-btn>
          <v-btn @click="showEditDialog = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      baseUrl: 'http://127.0.0.1:5000/',
      formData: {
        Titulo: '',
        Descripcion: '',
        Precio: null,
        Id_Categoria: null,
      },
      editData: {},
      menuItems: [],
      categorias: [
        { text: 'Entrada', value: 1 },
        { text: 'Plato Fuerte', value: 2 },
        { text: 'Postre', value: 3 },
      ],
      headers: [
        { text: 'Título', value: 'Titulo' },
        { text: 'Descripción', value: 'Descripcion' },
        { text: 'Precio', value: 'Precio' },
        { text: 'Acciones', value: 'acciones', sortable: false },
      ],
      valid: false,
      showPreview: false,
      showEditDialog: false,
    };
  },
  mounted() {
    this.getMenuItems();
  },
  methods: {
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

      const url = this.baseUrl + 'menu';
      const request = new Request(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.formData),
      });

      try {
        const response = await fetch(request);
        if (response.ok) {
          Swal.fire({
            title: '¡Platillo Agregado!',
            text: 'Se ha agregado un nuevo platillo exitosamente',
            icon: 'success',
          });
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
      const url = this.baseUrl + `menu/${this.editData.Id}`;
      const request = new Request(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.editData),
      });

      try {
        const response = await fetch(request);
        if (response.ok) {
          Swal.fire({
            title: '¡Platillo Actualizado!',
            text: 'El platillo ha sido actualizado exitosamente',
            icon: 'success',
          });
          this.getMenuItems();
          this.showEditDialog = false;
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
        this.editData = { ...item };
        this.showEditDialog = true;
      }
    },
    getCategoriaName(id) {
      const categoria = this.categorias.find(cat => cat.value === id);
      return categoria ? categoria.text : 'N/A';
    },
  },
};
</script>

<style scoped>
.v-btn {
  margin: 10px;
}
</style>
