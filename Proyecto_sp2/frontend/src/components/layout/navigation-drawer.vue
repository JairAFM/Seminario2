<template>
    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
      :color="drawerColor"
    >
      <v-list-item nav>
        <template v-slot:prepend v-if="rail">            
            <v-list-item prepend-icon="mdi-chevron-right" class="pa-2"></v-list-item>
        </template>
        <div v-if="false">
            <div class="d-flex justify-center">
                <v-icon icon="mdi-account-circle" size="5rem"></v-icon>
            </div>
            <div class="d-flex justify-center">
                <v-btn size="large" variant="flat" elevated color="primary" append-icon="mdi-login">Inicia Sesión</v-btn>
            </div>
            <div class="d-flex justify-center">
                <v-btn size="large" variant="flat" elevated color="primary" append-icon="mdi-account-plus">Registrate</v-btn>
            </div>
        </div>
        <template v-slot:append>
          <v-btn
            icon="mdi-chevron-left"
            variant="text"
            @click.stop="rail = !rail"
          ></v-btn>
        </template>
      </v-list-item>
      <v-divider></v-divider>
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-silverware-fork-knife" title="Menu" value="menu" to="/"></v-list-item>
        <v-list-item prepend-icon="mdi-tag-multiple" title="Promos" value="promos" to="/promos"></v-list-item>
        <v-list-item prepend-icon="mdi-calendar-month" title="Reservar" value="reservar" to="/reservation"></v-list-item>
        <v-list-item prepend-icon="mdi-motorbike" title="Domicilio" value="domicilio"></v-list-item>
        <v-list-item prepend-icon="mdi-tools" title="Mantenimientos" value="mantenimientos" to="/maintenances" v-if="isAuthenticated"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </template>
  <script>
    export default {
      data () {
        return {
          drawer: true,
          rail: true,
          drawerColor: '#ffeb3b',
        }
      },
      mounted() {
        const savedColor = localStorage.getItem('appBarColor');
        if (savedColor) {
          this.drawerColor = savedColor;
        }
      },
      watch: {
        '$localStorage.appBarColor': {
          handler(newColor) {
            if (newColor) {
              this.drawerColor = newColor;
            }
          },
          deep: true
        }
      },
      computed: {
          // Verifica si el token está almacenado en localStorage
          isAuthenticated() {
              return !!localStorage.getItem('token');
          },
          isAuthenticated() {
              return localStorage.getItem('tipoUser') == 0;
          }
      }
    }
  </script>