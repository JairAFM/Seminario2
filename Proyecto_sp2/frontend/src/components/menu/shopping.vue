<template>
    <div>
      <!-- Botón para abrir el carrito -->
      <v-btn @click="openCart" color="primary">Ver Carrito</v-btn>
  
      <!-- Diálogo del carrito -->
      <v-dialog v-model="cartDialog" max-width="800px">
        <v-card>
          <v-card-title class="text-h6">Carrito de Compras</v-card-title>
          <v-card-text>
            <!-- Tabla con Vuetify -->
            <v-data-table
              :headers="headers"
              :items="cartItems"
              item-value="Id"
              class="elevation-1"
            >
              <template v-slot:[`item.finalPrice`]="{ item }">
                <span>{{ formatPrice(item.finalPrice) }}</span>
              </template>
              <template v-slot:[`item.subtotal`]="{ item }">
                <span>{{ formatPrice(item.subtotal) }}</span>
              </template>
            </v-data-table>
  
            <!-- Área de pago -->
            <v-divider class="my-4"></v-divider>
            <div class="payment-section">
              <h4 class="text-h6 mb-4">Realizar Pago</h4>
  
              <!-- Opciones de entrega -->
              <v-radio-group v-model="deliveryOption" row>
                <v-radio label="Pago en el establecimiento" value="in-store"></v-radio>
                <v-radio label="Solicitar a domicilio" value="delivery"></v-radio>
              </v-radio-group>
  
              <!-- Información de tarjeta -->
              <v-text-field
                label="Nombre en la tarjeta"
                v-model="cardName"
                outlined
                class="mt-4"
              ></v-text-field>
              <v-text-field
                label="Número de tarjeta"
                v-model="cardNumber"
                outlined
                class="mt-3"
                maxlength="16"
              ></v-text-field>
              <v-row>
                <v-col cols="6">
                  <v-text-field
                    label="Fecha de expiración (MM/AA)"
                    v-model="cardExpiry"
                    outlined
                    class="mt-3"
                    maxlength="5"
                  ></v-text-field>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    label="Código de seguridad (CVV)"
                    v-model="cardCVV"
                    outlined
                    class="mt-3"
                    maxlength="3"
                  ></v-text-field>
                </v-col>
              </v-row>
  
              <!-- Botón de pago -->
              <v-btn
                class="mt-4"
                color="success"
                block
                @click="processPayment"
                :disabled="!isPaymentValid"
              >
                Pagar Q {{ formatPrice(total) }}
              </v-btn>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="closeCart">Cerrar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        cartDialog: false,
        deliveryOption: "in-store",
        cardName: "",
        cardNumber: "",
        cardExpiry: "",
        cardCVV: "",
        cartData: JSON.parse(`[{"Categoria":"Almuerzos","Descripcion":"Una jugosa y tierna carne a la parrilla, preparada con la mezcla perfecta de especias, servida en un suave pan artesanal. Acompañada de lechuga fresca, rodajas de tomate maduro, cebolla caramelizada y queso derretido. Complementada con un toque de mayonesa, mostaza y ketchup para resaltar los sabores. Ideal para disfrutar con papas fritas crujientes y una bebida refrescante.","FechaFin_Promo":null,"FechaIni_Promo":null,"Id":1,"Id_Categoria":1,"Imagenes":["ham1.jpg","ham2.jpg"],"Precio":"55.00","Precio_Promo":null,"Promo":0,"Titulo":"Hamburguesa","cantidad":2}]`),
        headers: [
          { text: "Producto", value: "Titulo" },
          { text: "Precio", value: "finalPrice" },
          { text: "Cantidad", value: "cantidad" },
          { text: "Subtotal", value: "subtotal" },
        ],
      };
    },
    computed: {
      cartItems() {
        return this.cartData.map((item) => {
          const finalPrice = item.Promo && item.Precio_Promo ? parseFloat(item.Precio_Promo) : parseFloat(item.Precio);
          const subtotal = finalPrice * item.cantidad;
          return { ...item, finalPrice, subtotal };
        });
      },
      total() {
        return this.cartItems.reduce((acc, item) => acc + item.subtotal, 0);
      },
      isPaymentValid() {
        return (
          this.cardName &&
          this.cardNumber.length === 16 &&
          this.cardExpiry.length === 5 &&
          this.cardCVV.length === 3
        );
      },
    },
    methods: {
      openCart() {
        this.cartDialog = true;
      },
      closeCart() {
        this.cartDialog = false;
      },
      processPayment() {
        if (this.deliveryOption === "in-store") {
          alert("El pago se realizará en el establecimiento.");
        } else {
          alert("El pedido será enviado a domicilio.");
        }
        this.closeCart();
      },
      formatPrice(value) {
        return `Q ${value.toFixed(2)}`;
      },
    },
  };
  </script>
  
  <style scoped>
  .payment-section {
    margin-top: 16px;
  }
  </style>
  