<template>
    <v-container>
      <v-card>
        <v-card-title>
          Mantenimiento de Empleados
          <v-spacer></v-spacer>
          <v-btn @click="openDialog('add')" color="primary" append-icon="mdi-plus">Agregar</v-btn>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="empleados"
          item-value="id"
          class="elevation-1"
          items-per-page-text="Registros por página"
          no-data-text="No se han encontrado empleados disponibles"
          :items-per-page-options="[{ value: 10, title: '10' }, { value: 20, title: '20' }, { value: 30, title: '30' }]"
        >
          <template v-slot:item.id_imagen="{ value }">
              <v-img
                :width="50"
                aspect-ratio="1/1"
                cover
                :src="baseUrl + 'uploads/' + value"
              ></v-img>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-btn icon @click="openDialog('edit', item)" class="mx-2">
              <v-icon color="green">mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteEmpleado(item.id, item.usuario)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
      <v-dialog v-model="dialog" style="max-width: 800px; z-index: 0;">
        <v-card>
          <v-card-title>
            <span v-if="dialogType === 'add'">Agregar Empleado</span>
            <span v-else>Editar Empleado</span>
          </v-card-title>
          <v-card-text>
            <v-row>
                <v-col cols="12" md="6">
                <v-text-field v-model="form.nombres" label="Nombres" required></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                <v-text-field v-model="form.apellidos" label="Apellidos" required></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                <v-text-field v-model="form.telefono" label="Teléfono" type="number"></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                <v-text-field v-model="form.salario" label="Salario" type="number" required></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                <v-text-field v-model="form.usuario" label="Usuario" required :disabled="dialogType === 'edit' ? true : false"></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                <v-text-field v-model="form.email" label="Email" required></v-text-field>
                </v-col>
                <v-col>
                  <v-combobox
                    clearable
                    label="Puesto"
                    item-title="description"
                    item-value="id"
                    v-model="form.puesto"
                    :items="Puestos"
                  ></v-combobox>
                </v-col>
                <v-col cols="12" md="6">
                    <v-file-input
                        @change="onFileChange"
                        label="Imagen del empleado"
                        accept="image/*"
                        prepend-icon="mdi-camera"
                        required
                    ></v-file-input>
                </v-col>
                <v-col cols="12" v-if="dialogType === 'edit'" class="d-flex justify-center align-center flex-column">
                  <h4>Imagen Actual</h4>
                  <v-img

                    :width="400"
                    aspect-ratio="1/1"
                    cover
                    :src="baseUrl + 'uploads/' + form.id_imagen"
                  ></v-img>
                </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" text @click="closeDialog">Cancelar</v-btn>
            <v-btn color="blue darken-1" text @click="saveEmpleado">Guardar</v-btn>
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
          { title: '', key: 'id_imagen' },
          { title: 'ID', key: 'id' },
          { title: 'Email', key: 'email' },
          { title: 'Nombres', key: 'nombres' },
          { title: 'Apellidos', key: 'apellidos' },
          { title: 'Telefono', key: 'telefono' },
          { title: 'Puesto', key: 'puesto' },
          { title: 'Salario', key: 'salario' },
          { title: 'Usuario', key: 'usuario' },
          { title: 'Acciones', key: 'actions', align: 'center', sortable: false }
        ],
        empleados: [],
        dialog: false,
        dialogType: 'add',
        form: {
          id: null,
          email: '',
          nombres: '',
          apellidos: '',
          telefono: null,
          salario: 0,
          usuario: '',
          puesto: null,
          image: null,
          mimetype: null
        },
        Puestos: [],
      };
    },
    mounted() {
      this.getEmpleados();
    },
    methods: {
      onFileChange(event) {
        const file = event.target.files[0];
        if (file) {
          this.form.mimetype = file.type.split('/')[1];
          const reader = new FileReader();
          reader.onloadend = () => {
            this.form.image = reader.result.split(',')[1];
          };
          reader.readAsDataURL(file); // Converts the file to a base64 string
        }
      },
      validateForm() {
            if (!this.form.nombres) {
            Swal.fire('Error', 'El campo "Nombres" es requerido', 'error');
            return false;
            }
            if (!this.form.apellidos) {
            Swal.fire('Error', 'El campo "Apellidos" es requerido', 'error');
            return false;
            }
            if (!this.form.telefono || this.form.telefono <= 0) {
            Swal.fire('Error', 'El campo "Teléfono" es requerido y debe ser un número válido', 'error');
            return false;
            }
            if (!this.form.salario || this.form.salario <= 0) {
            Swal.fire('Error', 'El campo "Salario" es requerido y debe ser un número mayor a 0', 'error');
            return false;
            }
            if (!this.form.usuario) {
            Swal.fire('Error', 'El campo "Usuario" es requerido', 'error');
            return false;
            }
            if (!this.form.email) {
            Swal.fire('Error', 'El campo "Email" es requerido', 'error');
            return false;
            }
            if (!this.form.puesto) {
            Swal.fire('Error', 'El campo "Puesto" es requerido', 'error');
            return false;
            }
            return true;
      },
      async getEmpleados() {
        const url = this.baseUrl + "getEmpleados";
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
          this.empleados = json;
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
        this.getPuestos();
        this.dialogType = type;
        if (type === 'edit' && item) {
          this.form = { ...item };
        } else {
          this.form = {
            id: null,
            email: '',
            nombres: '',
            apellidos: '',
            telefono: null,
            salario: 0,
            usuario: '',
            puesto: null,
            image: null,
            mimetype: null
          }
        }
        this.dialog = true;
      },
      closeDialog() {
        this.dialog = false;
      },
      async saveEmpleado() {
        const url = this.dialogType === 'add' ? this.baseUrl + 'newEmpleado' : `${this.baseUrl}editEmpleado/${this.form.id}`;
        const method = this.dialogType === 'add' ? 'POST' : 'PUT';
        if (!this.validateForm()) {
            return; // Stop the form submission if validation fails
        }
        this.form.puesto = this.form.puesto.id;
        try {
          const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.form),
          });
          console.log(response);
          if (response.ok) {
            Swal.fire('Éxito', `Empleado ${this.dialogType === 'add' ? 'creado' : 'actualizado'} exitosamente`, 'success');
            this.getEmpleados();
          } else {
            const errorData = await response.json();
            Swal.fire('Error', `Error al ${this.dialogType === 'add' ? 'crear' : 'actualizar'} empleado <br> ${errorData.error}`, 'error');
          }
        } catch (error) {
          Swal.fire('Error', `Error al ${this.dialogType === 'add' ? 'crear' : 'actualizar'} empleado`, 'error');
        }
  
        this.closeDialog();
      },
      async deleteEmpleado(id, usuario) {
        try {
          const response = await fetch(`${this.baseUrl}deleteEmpleado/${id}/${usuario}`, {
            method: 'DELETE',
          });
  
          if (response.ok) {
            Swal.fire('Éxito', 'Empleado eliminado exitosamente', 'success');
            this.getEmpleados();
          } else {
            Swal.fire('Error', 'Error al eliminar el empleado', 'error');
          }
        } catch (error) {
          Swal.fire('Error', 'Error al eliminar el empleado', 'error');
        }
      },
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
        this.Puestos = json;
      } catch (error) {
        Swal.fire({
          title: '¡Ha ocurrido un error!',
          text: 'Ocurrió un error al intentar cargar los datos',
          icon: 'error'
        });
      }
    },
    },
  };
  </script>
  