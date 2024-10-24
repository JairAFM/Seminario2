<template>
    <v-app-bar
        color="amber-lighten-3"
      >
        <v-app-bar-title>
            <v-btn variant="plain" to="/">
                <template v-slot:prepend>            
                    <v-img
                    :width="50"
                    aspect-ratio="4/3"
                    cover
                    src="../../assets/images/findTable.png"
                    rounded="circle"
                    ></v-img>
                </template> 
                findTable
            </v-btn>
        </v-app-bar-title>
        <v-spacer></v-spacer>
                <div class="text-center" v-if="isAuthenticated">
                    <v-btn 
                        size="small" 
                        variant="flat" 
                        color="light-blue-lighten-3" 
                        append-icon="mdi-logout"
                        class="me-2"
                        @click="logout"
                    >
                        Cerrar Sesión
                    </v-btn>
                </div>
                <div class="text-center" v-else>
                    <v-dialog max-width="500">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn 
                                size="small" 
                                variant="flat" 
                                color="light-blue-lighten-3" 
                                append-icon="mdi-login" 
                                v-bind="activatorProps"
                                class="me-2"
                            >
                                Inicia Sesión
                            </v-btn>
                        </template>
                        <template v-slot:default="{ isActive }">
                            <v-card 
                                    class="mx-auto"
                                    min-width="500"
                                >
                                <v-card-title 
                                    style="background-color: #ffe082;"
                                    class="mb-2 text-center"
                                >
                                    Inicia Sesión
                                </v-card-title>
                                <v-list class="pa-3">
                                    <v-form
                                        v-model="form"
                                        @submit.prevent="singIn"
                                    >
                                        <v-text-field
                                            class="mb-2"
                                            v-model="email"
                                            :rules="emailRules"
                                            label="Correo Electrónico"
                                            variant="outlined"
                                            required
                                            clearable
                                        ></v-text-field>
                                        <v-text-field
                                            class="mb-2"
                                            v-model="password"
                                            :readonly="loading"
                                            :rules="passRules"
                                            :type="showPassword ? 'text' : 'password'"
                                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                            @click:append="showPassword = !showPassword"
                                            label="Contraseña"
                                            variant="outlined"
                                            clearable
                                            required
                                        ></v-text-field>
                                        <v-btn
                                            :loading="loading"
                                            color="green-lighten-1"
                                            size="large"
                                            type="submit"
                                            variant="elevated"
                                            block
                                        >
                                            Iniciar Sesión
                                        </v-btn>
                                        <hr class="my-2"/>
                                        <p class="my-2 text-center" style="color:#424EFC;">
                                            ¿No tienes una cuenta?
                                        </p>
                                        <v-btn
                                            size="large"
                                            variant="elevated"
                                            color="light-blue-lighten-3"
                                            block
                                            to="/crearCuenta"
                                            @click="isActive.value = false"
                                        >
                                            Crear Cuenta
                                        </v-btn>
                                    </v-form>
                                </v-list>
                            </v-card>
                        </template>
                    </v-dialog>
                </div>
    </v-app-bar>
</template>
<script>
    export default {
        data: () => ({
            baseUrl: 'http://127.0.0.1:5000/',
            menu: false,
            form: false,
            email: '',
            emailRules: [
                value => {
                    if (value) return true
                    return 'El correo electrónico es requerido.'
                },
                value => {
                    if (/.+@.+\..+/.test(value)) return true
                    return 'El correo electrónico es inválido.'
                },
            ],
            password: null,
            passRules: [
                value => {
                    if (value) return true
                    return 'La contraseña es requerida.'
                },
            ],
            loading: false,
            showPassword: false,
        }),
        methods: {
            async singIn() {
                try {
                    // Muestra que se está iniciando la sesión (puedes usar un spinner o algo visual aquí)
                    this.loading = true;

                    const response = await fetch(this.baseUrl + 'login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            username: this.email,  // Cambiado a 'username' para coincidir con el back-end
                            password: this.password,
                        }),
                    });

                    const data = await response.json();

                    if (response.ok && data.token) {
                        // Almacenar token en localStorage para mantener la sesión
                        localStorage.setItem('tipoUser', data.data.Tipo_User);
                        localStorage.setItem('token', data.token);
                        location.reload();
                    } else {
                        // Manejo de errores si no se encontró el usuario o la contraseña es incorrecta
                        alert(data.message || 'Login failed');
                    }
                } catch (error) {
                    console.error('Error during login:', error);
                    alert('An error occurred during login.');
                } finally {
                    // Finaliza el estado de carga (oculta el spinner)
                    this.loading = false;
                }
            },
            logout() {
                localStorage.removeItem('tipoUser');
                localStorage.removeItem('token');
                location.reload();
            }
        },
        computed: {
            // Verifica si el token está almacenado en localStorage
            isAuthenticated() {
                return !!localStorage.getItem('token');
            }
        }
    }
</script>