<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        <h2>Configuración</h2>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form.color"
            label="Color"
            outlined
            required
            :bg-color="form.color"
            @click="colorMenu = true"
          ></v-text-field>
          <v-textarea
            v-model="form.descripcion"
            label="Descripción"
            outlined
            rows="4"
            required
          ></v-textarea>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" :disabled="!valid" @click="saveConfiguracion">
          Guardar
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Diálogo con la paleta de colores -->
    <v-dialog v-model="colorMenu" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Selecciona un color</v-card-title>
        <v-card-text>
          <v-color-picker v-model="form.color" flat hide-input></v-color-picker>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" text @click="applyColor">Aplicar</v-btn>
          <v-btn color="red" text @click="colorMenu = false">Cancelar</v-btn>
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
      valid: false,
      colorMenu: false, // Controla la visibilidad del diálogo con la paleta de colores
      form: {
        id: null,
        color: '#ffffff',
        descripcion: '',
      },
    };
  },
  mounted() {
    this.fetchConfiguracion();
  },
  methods: {
    async fetchConfiguracion() {
      try {
        const response = await fetch('http://127.0.0.1:5000/getConfiguracion');
        if (response.ok) {
          const data = await response.json();
          this.form.id = data.id;
          this.form.color = data.color;
          this.form.descripcion = data.descripcion;
        } else {
          Swal.fire({
            title: 'Configuración no encontrada',
            text: 'No se encontró la configuración. Por favor, ingrese una nueva.',
            icon: 'info',
          });
        }
      } catch (error) {
        Swal.fire({
          title: 'Error',
          text: 'No se pudo obtener la configuración. Inténtelo nuevamente más tarde.',
          icon: 'error',
        });
      }
    },
    async saveConfiguracion() {
      const url = 'http://127.0.0.1:5000/configTr';
      const opcion = this.form.id ? 2 : 1;

      try {
        const body = {
          color: this.form.color,
          descripcion: this.form.descripcion,
          opcion,
        };

        // Solo agrega el ID si es una actualización
        if (opcion === 2) {
          body.id = this.form.id;
        }

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });

        if (response.ok) {
          const result = await response.json();
          Swal.fire({
            title: 'Éxito',
            text: result.message,
            icon: 'success',
          });
          location.reload();
        } else {
          const error = await response.json();
          console.error('Error en el servidor:', error);
          Swal.fire({
            title: 'Error',
            text: error.error || 'No se pudo guardar la configuración.',
            icon: 'error',
          });
        }
      } catch (error) {
        console.error('Error en la solicitud:', error);
        Swal.fire({
          title: 'Error',
          text: 'No se pudo guardar la configuración. Inténtelo nuevamente más tarde.',
          icon: 'error',
        });
      }
    },

    applyColor() {
      this.colorMenu = false; // Cierra el diálogo
    },
  },
};
</script>

<style scoped>
.pa-4 {
  padding: 16px;
}
</style>
