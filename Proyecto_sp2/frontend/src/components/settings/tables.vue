<template>
    <v-container>
      <v-card>
        <v-card-title>
          Mantenimiento de Mesas
          <v-spacer></v-spacer>
          <v-btn @click="openDialog('add')" color="primary" append-icon="mdi-plus">Agregar</v-btn>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="mesas"
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
            <v-btn icon @click="deleteMesa(item.id)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span v-if="dialogType === 'add'">Agregar Mesa</span>
            <span v-else>Editar Mesa</span>
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="form.capacidad" label="Capacidad" required></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" text @click="closeDialog">Cancelar</v-btn>
            <v-btn color="blue darken-1" text @click="saveMesa">Guardar</v-btn>
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
          { title: 'Capacidad', key: 'capacidad' },
          { title: 'Acciones', align: 'center', key: 'actions', sortable: false },
        ],
        mesas: [],
        dialog: false,
        dialogType: 'add',
        form: {
          id: null,
          capacidad: '',
        },
      };
    },
    mounted() {
      this.getMesas();
    },
    methods: {
      async getMesas() {
        const url = this.baseUrl + 'getMesas';
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
          this.mesas = json;
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
          this.form = { id: null, capacidad: '' };
        }
        this.dialog = true;
      },
      closeDialog() {
        this.dialog = false;
      },
      async saveMesa() {
        if (!this.form.capacidad) {
          Swal.fire({
            title: '¡Advertencia!',
            text: 'Los campos no pueden estar vacíos',
            icon: 'warning'
          });
          return null;
        }
  
        if (this.dialogType === 'add') {
          const url = this.baseUrl + 'newMesa';
          const request = new Request(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              capacidad: this.form.capacidad
            }),
          });
  
          const response = await fetch(request);
          if (response.status === 200) {
            Swal.fire({
              title: '¡Mesa Creada!',
              text: 'Se ha creado una nueva mesa exitosamente',
              icon: 'success'
            });
            this.getMesas();
          } else {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al crear la mesa',
              icon: 'error'
            });
          }
        } else if (this.dialogType === 'edit') {
          const url = this.baseUrl + `editMesa/${this.form.id}`;
          const request = new Request(url, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              capacidad: this.form.capacidad
            }),
          });
  
          const response = await fetch(request);
          if (response.status === 200) {
            Swal.fire({
              title: '¡Mesa Actualizada!',
              text: 'Mesa actualizada exitosamente',
              icon: 'success'
            });
            this.getMesas();
          } else {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al actualizar la mesa',
              icon: 'error'
            });
          }
        }
  
        this.closeDialog();
      },
      async deleteMesa(id) {
        try {
          const url = this.baseUrl + `deleteMesa/${id}`;
          const response = await fetch(url, { method: 'DELETE' });
  
          if (response.ok) {
            Swal.fire({
              title: '¡Mesa Eliminada!',
              text: 'La mesa ha sido eliminada exitosamente',
              icon: 'success'
            });
            this.getMesas();
          } else if (response.status === 404) {
            Swal.fire({
              title: '¡Mesa No Encontrada!',
              text: 'No se encontró la mesa que desea eliminar',
              icon: 'warning'
            });
          } else {
            Swal.fire({
              title: '¡Ha ocurrido un error!',
              text: 'Ocurrió un error al eliminar la mesa',
              icon: 'error'
            });
          }
        } catch (error) {
          Swal.fire({
            title: '¡Ha ocurrido un error!',
            text: 'Ocurrió un error al eliminar la mesa',
            icon: 'error'
          });
        }
      },
    },
  };
  </script>
  