<template>
    <v-app-bar :color="appBarColor">
      <v-app-bar-title>
        <v-btn variant="plain" to="/">
          <template v-slot:prepend>            
            <v-img
              :width="50"
              aspect-ratio="4/3"
              cover
              src="../../assets/images/findTable.png"
              rounded="circle"
            ></v-img>
          </template> 
          findTable
        </v-btn>
      </v-app-bar-title>
      <v-spacer></v-spacer>
  
      <!-- Botón para abrir la paleta de colores -->
      <v-btn @click="colorMenu = true" variant="flat" color="primary">Cambiar color</v-btn>
  
      <!-- Diálogo con la paleta de colores -->
      <v-dialog v-model="colorMenu" max-width="400">
        <v-card>
          <v-card-title class="text-h6">Selecciona un color</v-card-title>
          <v-card-text>
            <v-color-picker
              v-model="selectedColor"
              flat
              hide-input
            ></v-color-picker>
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" text @click="applyColor">Aplicar</v-btn>
            <v-btn color="red" text @click="colorMenu = false">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  
      <div class="text-center" v-if="isAuthenticated">
        <v-btn 
          size="small" 
          variant="flat" 
          color="light-blue-lighten-3" 
          append-icon="mdi-logout"
          class="me-2"
          @click="logout"
        >
          Cerrar Sesión
        </v-btn>
      </div>
      <div class="text-center" v-else>
        <v-dialog max-width="500">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn 
              size="small" 
              variant="flat" 
              color="light-blue-lighten-3" 
              append-icon="mdi-login" 
              v-bind="activatorProps"
              class="me-2"
            >
              Inicia Sesión
            </v-btn>
          </template>
          <template v-slot:default="{ isActive }">
            <v-card 
              class="mx-auto"
              min-width="500"
            >
              <v-card-title 
                style="background-color: #ffe082;"
                class="mb-2 text-center"
              >
                Inicia Sesión
              </v-card-title>
              <v-list class="pa-3">
                <v-form
                  v-model="form"
                  @submit.prevent="singIn"
                >
                  <v-text-field
                    class="mb-2"
                    v-model="email"
                    :rules="emailRules"
                    label="Correo Electrónico o Usuario"
                    variant="outlined"
                    required
                    clearable
                  ></v-text-field>
                  <v-text-field
                    class="mb-2"
                    v-model="password"
                    :readonly="loading"
                    :rules="passRules"
                    :type="showPassword ? 'text' : 'password'"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="showPassword = !showPassword"
                    label="Contraseña"
                    variant="outlined"
                    clearable
                    required
                  ></v-text-field>
                  <v-btn
                    :loading="loading"
                    color="green-lighten-1"
                    size="large"
                    type="submit"
                    variant="elevated"
                    block
                  >
                    Iniciar Sesión
                  </v-btn>
                  <hr class="my-2"/>
                  <p class="my-2 text-center" style="color:#424EFC;">
                    ¿No tienes una cuenta?
                  </p>
                  <v-btn
                    size="large"
                    variant="elevated"
                    color="light-blue-lighten-3"
                    block
                    to="/crearCuenta"
                    @click="isActive.value = false"
                  >
                    Crear Cuenta
                  </v-btn>
                </v-form>
              </v-list>
            </v-card>
          </template>
        </v-dialog>
      </div>
    </v-app-bar>
  </template>
  
  <script>
  export default {
    data() {
      return {
        appBarColor: '#ffeb3b', // Color inicial de la barra de navegación
        selectedColor: '#ffeb3b', // Color seleccionado en el picker
        colorMenu: false, // Controla la visibilidad del diálogo con la paleta de colores
        email: '',
        password: null,
        loading: false,
        emailRules: [
          value => (value ? true : 'El correo electrónico o usuario es requerido.'),
        ],
        passRules: [
          value => (value ? true : 'La contraseña es requerida.'),
        ],
        showPassword: false,
        form: null,
      };
    },
    mounted() {
      // Cargar el color guardado en localStorage si existe
      const savedColor = localStorage.getItem('appBarColor');
      if (savedColor) {
        this.appBarColor = savedColor;
        this.selectedColor = savedColor;
      }
    },
    methods: {
      applyColor() {
        // Actualizar el color de la barra de navegación y guardar en localStorage
        this.appBarColor = this.selectedColor;
        localStorage.setItem('appBarColor', this.selectedColor);
        this.colorMenu = false; // Cerrar el diálogo
      },
      logout() {
        localStorage.removeItem('token');
        location.reload();
      },
    },
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('token');
      },
    },
  };
  </script>
  