<template>
    <v-app-bar
        color="primary"
      >
        <v-app-bar-title>
            <v-btn variant="text" to="/">
                Restaurante-X
            </v-btn>
        </v-app-bar-title>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon icon="mdi-magnify"></v-icon>
        </v-btn>
        
        <v-btn variant="flat" color="primary" append-icon="mdi-login">Inicia Sesión</v-btn>
        <v-btn variant="flat" color="primary" append-icon="mdi-account-plus">Registrate</v-btn>
      </v-app-bar>
</template>