<template>
  <v-card
    color="primary"
    variant="elevated"
    class="mx-auto custom-card"
    style="width: 220px; height: auto;"
  >
    <v-card-item>
      <div class="text-center">
        <!-- Icono dinámico -->
        <div class="d-flex justify-center">
          <v-icon :icon="icon" size="5rem" class="custom-icon"></v-icon>
        </div>
        <!-- Título -->
        <div class="d-flex justify-center text-h6 mb-1">
          {{ title }}
        </div>
        <!-- Descripción -->
        <div class="d-flex justify-center text-caption">
          {{ descrip }}
        </div>
      </div>
    </v-card-item>
    <v-card-actions class="d-flex justify-end">
      <!-- Botón con enlace dinámico -->
      <v-btn :to="link" class="custom-btn">
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

<style scoped>
.custom-card {
  background: linear-gradient(135deg, #039CE8, #74b9ff);
  color: white;
  border-radius: 27px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 220px; /* Ajuste del ancho */
  height: auto; /* Ajuste automático de la altura */
}

.custom-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.custom-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(255, 255, 255, 0.15);
  clip-path: circle(100px at 50% 50%);
  transition: clip-path 0.3s ease;
  z-index: 0;
}

.custom-card:hover::before {
  clip-path: circle(300px at 50% 50%);
}

.custom-icon {
  font-size: 5rem;
  margin-bottom: 10px;
}

.custom-btn {
  background: #ffffff;
  color: #039CE8;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: bold;
  text-decoration: none;
  transition: background 0.3s ease, color 0.3s ease;
}

.custom-btn:hover {
  background: #039CE8;
  color: #ffffff;
}
</style>
