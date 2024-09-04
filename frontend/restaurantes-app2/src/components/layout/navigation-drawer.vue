<template>
    <v-navigation-drawer
      v-model="drawer"
      :rail="rail"
      permanent
      @click="rail = false"
      color="primary"
    >
      <v-list-item nav>
        <template v-slot:prepend v-if="rail">            
            <v-list-item prepend-icon="mdi-account-circle" class="pa-2"></v-list-item>
        </template>
        <div>
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
        <v-list-item prepend-icon="mdi-silverware-fork-knife" title="Menu" value="menu"></v-list-item>
        <v-list-item prepend-icon="mdi-tag-multiple" title="Promos" value="promos"></v-list-item>
        <v-list-item prepend-icon="mdi-calendar-month" title="Reservar" value="reservar"></v-list-item>
        <v-list-item prepend-icon="mdi-motorbike" title="Domicilio" value="domicilio"></v-list-item>
        <v-list-item prepend-icon="mdi-tools" title="Mantenimientos" value="mantenimientos" to="/maintenances"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </template>
  <script>
    export default {
      data () {
        return {
          drawer: true,
          rail: true,
        }
      },
    }
  </script>