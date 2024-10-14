<template>
  <v-card
    color="primary"
    variant="elevated"
    class="mx-auto"
    style="width: 350px; height: 250px;"
  >
    <v-card-item>
      <div>
        <div class="d-flex justify-center">
          <v-icon :icon="icon" size="5rem"></v-icon>
        </div>
        <div class="d-flex justify-center text-h6 mb-1">
          {{ title }}
        </div>
        <div class="d-flex justify-center text-caption">{{ descrip }}</div>
      </div>
    </v-card-item>
    <v-card-actions class="d-flex justify-end">
      <v-btn :to="link">
        Ir
        <v-icon icon="mdi-location-enter"></v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    title: String,
    descrip: String,
    link: String,
    icon: String
  }
}
</script>
