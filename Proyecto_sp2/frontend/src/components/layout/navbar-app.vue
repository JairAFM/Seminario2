<template>
  <v-app-bar :color="appBarColor">
    <v-btn variant="plain" to="/">
      <template v-slot:prepend>
        <v-img :width="50" aspect-ratio="4/3" cover src="../../assets/images/findTable.png" rounded="circle"></v-img>
      </template>
      SPOT2DINE
    </v-btn>

    <v-spacer></v-spacer>

    <v-btn class="text-none" stacked to="/">
      <v-icon>mdi-silverware-fork-knife</v-icon> Menú
    </v-btn>
    <v-btn class="text-none" stacked to="/promos"> 
      <v-icon>mdi-tag-multiple</v-icon> Promos
    </v-btn>
    <v-btn class="text-none" stacked to="/reservation"> 
      <v-icon>mdi-calendar-month</v-icon> Reserva ya!
    </v-btn>
    <v-btn class="text-none" stacked to="/maintenances" v-if="isAuthenticated_admin">
      <v-icon>mdi-tools</v-icon> Mantenimientos
    </v-btn>


    <v-spacer></v-spacer>
    <v-badge dot class="me-2" color="yellow">
      <v-btn size="small" variant="flat" color="light-blue-lighten-3" icon="mdi-cart-heart" @click="verCarrito">
      </v-btn>
    </v-badge>
    <div class="text-center" v-if="isAuthenticated">
      <v-btn size="small" variant="flat" color="light-blue-lighten-3" append-icon="mdi-logout" class="me-2"
        @click="logout">
        Cerrar Sesión
      </v-btn>
      </div>
      <div class="text-center" v-else>
        <v-dialog max-width="500">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn size="small" variant="flat" color="light-blue-lighten-3" append-icon="mdi-login"
              v-bind="activatorProps" class="me-2">
              Inicia Sesión
            </v-btn>
          </template>
          <template v-slot:default="{ isActive }">
            <v-card class="mx-auto" min-width="500">
              <v-card-title :style="'background-color:' + appBarColor" class="mb-2 text-center text-none">
                Inicia Sesión
              </v-card-title>
              <v-list class="pa-3">
                <v-form v-model="form" @submit.prevent="signIn">
                  <v-text-field class="mb-2" v-model="email" :rules="emailRules" label="Correo Electrónico o Usuario"
                    variant="outlined" required clearable></v-text-field>
                  <v-text-field class="mb-2" v-model="password" :readonly="loading" :rules="passRules"
                    :type="showPassword ? 'text' : 'password'" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="showPassword = !showPassword" label="Contraseña" variant="outlined" clearable
                    required></v-text-field>
                  <v-btn :loading="loading" color="green-lighten-1" size="large" type="submit" variant="elevated" block>
                    Iniciar Sesión
                  </v-btn>
                  <hr class="my-2" />
                  <p class="my-2 text-center" style="color:#424EFC;">
                    ¿No tienes una cuenta?
                  </p>
                  <v-btn size="large" variant="elevated" color="light-blue-lighten-3" block to="/crearCuenta"
                    @click="isActive.value = false">
                    Crear Cuenta
                  </v-btn>
                </v-form>
              </v-list>
            </v-card>
          </template>
        </v-dialog>
      </div>
    
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
            items-per-page-text="Registros por página"
          no-data-text="No se han encontrado datos disponibles"
          :items-per-page-options="[{value: 10, title: '10'},
                                    {value: 20, title: '20'},
                                    {value: 30, title: '30'}]"
          >
            <template v-slot:[`item.finalPrice`]="{ item }">
              <span>{{ formatPrice(item.finalPrice) }}</span>
            </template>
            <template v-slot:[`item.subtotal`]="{ item }">
              <span>{{ formatPrice(item.subtotal) }}</span>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
            <v-btn icon @click="deleteShop(item.Id)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
          </v-data-table>

          <v-divider class="my-4"></v-divider>
            <div class="payment-section" v-if="isAuthenticated">
              <h4 class="text-h6 mb-4">Realizar Pago</h4>
  
              <!-- Información de tarjeta -->
              <v-text-field
                label="Dirección"
                v-model="direction"
                outlined
                class="mt-3"
                maxlength="16"
              ></v-text-field>
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
                @click="pagar"
              >
                Pagar Q {{ formatPrice(total) }}
              </v-btn>
            </div>
            <div class="payment-section" v-else>  
              <v-alert
                density="compact"
                text="Debe iniciar sesión para poder completar su orden"
                title="Atención!"
                type="warning"
              ></v-alert>
            </div>
        </v-card-text>
        <v-card-actions>
          <div class="flex-grow-1 text-end">
            <p class="text-h6">Total: {{ formatPrice(total) }}</p>
          </div>
          <v-btn color="primary" @click="closeCart">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    </v-app-bar>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: null,
        loading: false,
        cartData: [],
        cartDialog: false,
        emailRules: [
          value => (value ? true : 'El correo electrónico o usuario es requerido.'),
        ],
        passRules: [
          value => (value ? true : 'La contraseña es requerida.'),
        ],
        showPassword: false,
        form: null,
        appBarColor: '#ffeb3b', // Color inicial de la barra de navegación
        headers: [
        { title: "Producto", key: "Titulo" },
        { title: "Cantidad", key: "cantidad" },
        { title: "Precio", key: "finalPrice" },
        { title: "Subtotal", key: "subtotal" },
        { title: 'Acciones', align: 'center', key: 'actions', sortable: false },
      ],
      direction: '',
      cardName: "",
      cardNumber: "",
      cardExpiry: "",
      cardCVV: "",
      };
    },
    mounted() {
      this.fetchConfiguracion();
      // Cargar el color guardado en localStorage si existe
      
    },
    methods: {
      async fetchConfiguracion() {
        try {
          const response = await fetch('http://127.0.0.1:5000/getConfiguracion');
          if (response.ok) {
            const data = await response.json();
            localStorage.setItem('appBarColor', data.color);
            const savedColor = data.color;
            if (savedColor) {
              this.appBarColor = savedColor;
            }
          }
        } catch (error) {
          console.log(error);
        }
      },
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('tipoUser');
        localStorage.removeItem('userId');
        location.reload();
      },
      async signIn() {
              try {
                  this.loading = true;
                  const response = await fetch('http://127.0.0.1:5000/login', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                          username: this.email,
                          password: this.password,
                      }),
                  });
                  const data = await response.json();
                  if (response.ok && data.token) {
                      localStorage.setItem('tipoUser', data.data.Tipo_User);
                      localStorage.setItem('token', data.token);
                      localStorage.setItem('userId', data.data.Id_User);
                      location.reload();
                  } else {
                      alert(data.message || 'Login failed');
                  }
              } catch (error) {
                  console.error('Error during login:', error);
                  alert('An error occurred during login.');
              } finally {
                  this.loading = false;
              }
          },
          verCarrito() {
            this.cartData = JSON.parse(localStorage.getItem("shopCart")) || [];
            this.cartDialog = true;
            
          },
          closeCart() {
            this.cartDialog = false;
          },
          formatPrice(value) {
            return `Q ${value.toFixed(2)}`;
          },
          deleteShop(id) {
            let existingArray = JSON.parse(localStorage.getItem("shopCart")) || [];
            if (existingArray.length > 0) {

                let filter = existingArray.filter(k => k.Id == id);
                if (filter.length > 0) {
                  if (filter[0].cantidad > 1) {
                    existingArray = existingArray.map((value, index) => {
                        if (value.Id == id) {
                            value.cantidad = value.cantidad - 1;
                        }
                        return value;
                    });
                    
                    localStorage.setItem("shopCart", JSON.stringify(existingArray));
                  this.cartData = existingArray;
                  } else {
                    filter = existingArray.filter(k => k.Id != id);
                    localStorage.setItem("shopCart", JSON.stringify(filter));
                  this.cartData = filter;
                  }
                }
                }
            
          },
          
      async pagar() {
              let total = this.cartItems.reduce((acc, item) => acc + item.subtotal, 0);
              try {
                  const response = await fetch('http://127.0.0.1:5000/guardarOrden', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({
                          Id_Cliente: localStorage.getItem('userId'),
                          Total: total,
                          Detalle: JSON.stringify(this.cartData)
                      }),
                  });
                  const data = await response.json();
                  if (response.Id_Orden) {
                      this.cartDialog = false;
                      localStorage.setItem('shopCart', JSON.stringify([]));
                      this.direction = '';
                      this.cardName = "";
                      this.cardNumber = "";
                      this.cardExpiry = "";
                      this.cardCVV = "";
                  } else {
                      this.cartDialog = false;
                      localStorage.setItem('shopCart', JSON.stringify([]));
                      this.direction = '';
                      this.cardName = "";
                      this.cardNumber = "";
                      this.cardExpiry = "";
                      this.cardCVV = "";
                      alert(data.message || 'eerror');
                  }
              } catch (error) {
                  console.error('Error during login:', error);
              } finally {
                  this.loading = false;
              }
          },


    },
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('token');
      },
  
      isAuthenticated_admin() {
        return localStorage.getItem('tipoUser') == 0;
      },
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
    },
  };
  </script>
