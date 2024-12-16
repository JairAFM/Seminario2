<template>
    <div class="reservation-details">
      <h1>Detalles de tus Reservas</h1>
      <table v-if="reservations.length > 0">
        <thead>
          <tr>
            <th>ID Mesa</th>
            <th>ID Orden</th>
            <th>Fecha Inicio</th>
            <th>Hora</th>
            <th>Número de Personas</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="reservation in reservations" :key="reservation.order_id">
            <td>{{ reservation.id_mesa }}</td>
            <td>{{ reservation.id_orden }}</td>
            <td>{{ reservation.inicio }}</td>
            <td>{{ reservation.hora }}</td>
            <td>{{ reservation.no_personas }}</td>
            <td>{{ reservation.descripcion }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No tienes reservas realizadas.</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        reservations: [],
        id_cliente: ""
      };
    },
    mounted(){
        this.isAuthenticated();
    },
    methods: {
        isAuthenticated() {
            this.id_cliente = localStorage.getItem('userId');
            //console.log("id " + this.id_cliente);
            this.fetchReservations();
        },
        async fetchReservations() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/verReservas/${this.id_cliente}`); 

                if (!response.ok) {
                    throw new Error(`Error al obtener las reservas: ${response.statusText}`);
                }

                const result = await response.json();

                if (result && result.length > 0) {
                    this.reservations = result.map(reservation => ({
                        ...reservation,
                        hora: this.formatSecondsToTime(reservation.hora),
                        inicio: this.formatDate(reservation.inicio) 
                    }));
                } else {
                    this.reservations = [];
                }
            } catch (error) {
                console.error("Error al cargar las reservas:", error);
            }
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const day = String(date.getDate() + 1).padStart(2, '0');
            const month = date.toLocaleString('en-US', { month: 'short' });
            const year = date.getFullYear(); 

            return `${day} ${month} ${year}`;
        },
        formatSecondsToTime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;

            return [
                String(hours).padStart(2, '0'),
                String(minutes).padStart(2, '0'),
                String(secs).padStart(2, '0')
            ].join(':');
        }
    },
  };
  </script>
  
  <style scoped>
  .reservation-details {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  th {
    background-color: #f4f4f4;
  }
  
  p {
    text-align: center;
    color: #555;
  }
  </style>
  
