<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        <h2>Configuración</h2>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            v-model="Color"
            label="Color"
            outlined
            required
            :bg-color="Color"
            @click="colorMenu = true"
          ></v-text-field>
          <v-textarea
            v-model="Descripcion"
            label="Descripción"
            outlined
            rows="4"
            required
          ></v-textarea>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" :disabled="!valid" @click="updateConfiguracion">
          Guardar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
  <!-- Diálogo con la paleta de colores -->
    <v-dialog v-model="colorMenu" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Selecciona un color</v-card-title>
        <v-card-text>
          <v-color-picker v-model="Color" flat hide-input></v-color-picker>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" text @click="applyColor">Aplicar</v-btn>
          <v-btn color="red" text @click="colorMenu = false">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      valid: false,
      colorMenu: false, // Controla la visibilidad del diálogo con la paleta de colores
      Color: '#ffeb3b',
      Descripcion: '',
    };
  },
  mounted() {
    this.fetchConfiguracion();
  },
  methods: {
    fetchConfiguracion() {
      // Suponiendo que el ID del único registro es siempre 1
      axios
        .get('/api/configuraciones/1')
        .then((response) => {
          this.formData = response.data || { Color: '', Descripcion: '' };
        })
        .catch(() => {
          alert('No se pudo cargar la configuración.');
        });
    },
    updateConfiguracion() {
      axios
        .put('/api/configuraciones/1', this.formData)
        .then(() => {
          alert('Configuración actualizada correctamente');
        })
        .catch(() => {
          alert('Error al actualizar la configuración.');
        });
    },
    applyColor() {
      localStorage.setItem('appBarColor', this.Color);
      this.colorMenu = false; // Cerrar el diálogo
    },
  },
};
</script>
