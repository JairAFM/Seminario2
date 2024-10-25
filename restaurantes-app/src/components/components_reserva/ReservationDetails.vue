<template>
    <div class="container mt-5">
      <h1 class="mb-4 text-center">Detalles de la Reservación</h1>
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Información de la Reservación</h5>
        </div>
        <div class="card-body">
          <div v-if="reservation">
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <strong>Fecha:</strong> {{ reservation.fecha_reserva }}
              </li>
              <li class="list-group-item">
                <strong>Hora:</strong> {{ reservation.hora_reserva }}
              </li>
              <li class="list-group-item">
                <strong>Número de Personas:</strong> {{ reservation.cantidad_personas }}
              </li>
              <li class="list-group-item">
                <strong>Número de Mesa:</strong> {{ reservation.mesa }}
              </li>
            </ul>
          </div>
          <div v-else>
            <p class="text-danger">No se encontró información sobre la reservación.</p>
          </div>
        </div>
        <div class="card-footer text-center">
          <router-link to="/" class="btn btn-secondary">Volver al inicio</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ReservationDetails',
    data() {
      return {
        reservation: null, // Para almacenar los detalles de la reserva
      };
    },
    mounted() {
      // Obtener el ID de la reserva de los parámetros de la ruta
      const reservationId = this.$route.params.id; // Cambia a params
      this.fetchReservationDetails(reservationId);
    },
    methods: {
      fetchReservationDetails(id) {
        // Llamar a la API para obtener los detalles de la reserva
        axios.get(`http://localhost:5000/get_reservas/${id}`)
          .then(response => {
            this.reservation = response.data; // Guardar los datos de la reserva
          })
          .catch(error => {
            console.error("Error al obtener los detalles de la reserva:", error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos personalizados */
  .card {
    border-radius: 10px;
  }
  .card-header {
    font-size: 1.25rem;
  }
  </style>
  