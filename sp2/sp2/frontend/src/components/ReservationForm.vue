<template>
  <div class="container mt-5">
    <h1 class="mb-4">Formulario de Reservación</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="date" class="form-label">Fecha:</label>
        <input type="date" id="date" v-model="reservation.date" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="time" class="form-label">Hora:</label>
        <input type="time" id="time" v-model="reservation.time" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="guests" class="form-label">Número de Personas:</label>
        <select id="guests" v-model="guestCount" class="form-select" required>
          <option value="" disabled selected>Elegir cantidad</option>
          <option :value="cantidad_sillas">Número de sillas de la mesa seleccionada ({{ cantidad_sillas }})</option>
          <option value="personalizado">Elegir cantidad personalizada</option>
        </select>
      </div>

      <!-- Mostrar el input solo si la opción es 'personalizado' -->
      <div v-if="guestCount === 'personalizado'" class="mb-3">
        <label for="customGuests" class="form-label">Cantidad:</label>
        <input type="number" id="customGuests" v-model="reservation.customGuests" class="form-control" required min="1" />
      </div>

      <button type="submit" class="btn btn-primary">Reservar</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'; // Importa axios

export default {
  name: 'ReservationForm',
  data() {
    return {
      guestCount: '', // Para almacenar la opción seleccionada
      reservation: { // Para almacenar los datos de la reserva
        date: '',
        time: '',
        customGuests: null,
        mesa: null, // Añadir la propiedad para el número de mesa
      },
      cantidad_sillas: 0, // Variable para almacenar la cantidad de sillas
    };
  },
  mounted() {
    const mesa = this.$route.query.mesa; // Obtener el número de mesa de los parámetros de consulta
    this.reservation.mesa = mesa; // Guardar el número de mesa en el objeto de reserva
    console.log('Número de mesa:', mesa);

    // Establecer la cantidad de sillas según el id de la mesa
    this.setSillaCount(mesa);
  },
  methods: {
    setSillaCount(mesaId) {
      switch (mesaId) {
        case '1':
          this.cantidad_sillas = 3;
          break;
        case '2':
          this.cantidad_sillas = 4;
          break;
        case '3':
          this.cantidad_sillas = 6;
          break;
        case '4':
          this.cantidad_sillas = 8;
          break;
        default:
          this.cantidad_sillas = 0; // O puedes asignar un valor por defecto
          break;
      }
    },
    submitForm() {
      // Definir el número de personas
      const numberOfGuests = this.guestCount === 'personalizado' ? this.reservation.customGuests : this.cantidad_sillas;

      // Preparar los datos a enviar, asegurando que el número de mesa sea un entero
      const dataToSend = {
        id_usuario: 1, // Cambia esto por el ID real del usuario
        id_estado: 1,  // Cambia esto por el ID real del estado de la reserva
        fecha_reserva: this.reservation.date,
        hora_reserva: this.reservation.time,
        cantidad_personas: numberOfGuests,
        mesa: parseInt(this.reservation.mesa, 10), // Convertir el número de mesa a entero
      };

      // Lógica para enviar el formulario
      console.log("Formulario enviado con los datos:", dataToSend);
      
      // Realizar la solicitud POST
      axios.post('http://localhost:5000/reservas', dataToSend)
        .then(response => {
          console.log("Reserva creada con éxito:", response.data);
        })
        .catch(error => {
          console.error("Error al crear la reserva:", error.response.data);
        });
    },
  },
};
</script>

<style scoped>
/* Estilos personalizados */
</style>
