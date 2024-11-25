<template>
    <v-container>
      <v-card>
        <v-card-title>
          Mantenimiento de Puestos
          <v-spacer></v-spacer>
          <v-btn @click="openDialog('add')" color="primary" append-icon="mdi-plus">Agregar</v-btn>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="puestos"
          item-value="id"
          class="elevation-1"
          items-per-page-text="Registros por página"
          no-data-text="No se han encontrado datos disponibles"
          :items-per-page-options="[{value: 10, title: '10'}, {value: 20, title: '20'}, {value: 30, title: '30'}]"
        >
          <template v-slot:[`item.actions`]="{ item }">
            <v-btn icon @click="openDialog('edit', item)" class="mx-2">
              <v-icon color="green">mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deletePuesto(item.id)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span v-if="dialogType === 'add'">Agregar Puesto</span>
            <span v-else>Editar Puesto</span>
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
            <v-btn color="blue darken-1" text @click="savePuesto">Guardar</v-btn>
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
      headers: [
        { title: 'ID', key: 'id' },
        { title: 'Descripción', key: 'description' },
        { title: 'Acciones', align: 'center', key: 'actions', sortable: false },
      ],
      puestos: [],
      dialog: false,
      dialogType: 'add',
      form: {
        id: null,
        description: '',
      },
    };
  },
  mounted() {
    this.getPuestos();
  },
  methods: {
    async getPuestos() {
      const url = this.baseUrl + 'getPuestos';
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
        this.puestos = json;
      } catch (error) {
        Swal.fire({
          title: '¡Ha ocurrido un error!',
          text: 'Ocurrió un error al intentar cargar los datos',
          icon: 'error'
        });
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
    async savePuesto() {
      if (!this.form.description) {
        Swal.fire({
          title: '¡Advertencia!',
          text: 'La descripción no puede ser nula',
          icon: 'warning'
        });
        return null;
      }

      if (this.dialogType === 'add') {
        const url = this.baseUrl + 'newPuesto';
        const request = new Request(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description: this.form.description }),
        });

        const response = await fetch(request);
        if (response.status === 200) {
          Swal.fire({
            title: '¡Puesto Creado!',
            text: 'Se ha creado un nuevo puesto exitosamente',
            icon: 'success'
          });
          this.getPuestos();
        } else {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al crear el puesto',
            icon: 'error'
          });
        }
      } else if (this.dialogType === 'edit') {
        const url = this.baseUrl + `editPuesto/${this.form.id}`;
        const request = new Request(url, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description: this.form.description }),
        });

        const response = await fetch(request);
        if (response.status === 200) {
          Swal.fire({
            title: '¡Puesto Actualizado!',
            text: 'Puesto actualizado exitosamente',
            icon: 'success'
          });
          this.getPuestos();
        } else {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al actualizar el puesto',
            icon: 'error'
          });
        }
      }

      this.closeDialog();
    },
    async deletePuesto(id) {
      try {
        const url = this.baseUrl + `deletePuesto/${id}`;
        const response = await fetch(url, { method: 'DELETE' });

        if (response.ok) {
          Swal.fire({
            title: '¡Puesto Eliminado!',
            text: 'El puesto ha sido eliminado exitosamente',
            icon: 'success'
          });
          this.getPuestos();
        } else if (response.status === 404) {
          Swal.fire({
            title: '¡Puesto No Encontrado!',
            text: 'No se encontró el puesto que desea eliminar',
            icon: 'warning'
          });
        } else {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al eliminar el puesto',
            icon: 'error'
          });
        }
      } catch (error) {
        Swal.fire({
          title: '¡Ha ocurrido un error!',
          text: 'Ocurrió un error al eliminar el puesto',
          icon: 'error'
        });
      }
    },
  },
};
</script> 