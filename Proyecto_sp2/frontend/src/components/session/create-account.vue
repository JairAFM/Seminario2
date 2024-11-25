<template>
    <v-row>
        <v-col cols="12" md="4" offset-md="4">
            <v-card 
                class="mx-auto"
                min-width="300"
            >
                <v-card-title 
                    style="background-color: #ffe082;"
                    class="mb-2 text-center"
                >
                    Crear Cuenta
                </v-card-title>
                <v-form
                    class="pa-1"
                    v-model="form"
                    @submit.prevent="createAccount"
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
                        v-model="phone"
                        :rules="phoneRules"
                        label="Número de Teléfono"
                        type="tel"
                        variant="outlined"
                        maxlength="10"
                        required
                        clearable
                    ></v-text-field>
                    <v-text-field
                        class="mb-2"
                        v-model="name"
                        :rules="nameRules"
                        label="Nombres"
                        variant="outlined"
                        clearable
                        required
                    ></v-text-field>
                    <v-text-field
                        class="mb-2"
                        v-model="lastName"
                        :rules="lastNRules"
                        label="Apellidos"
                        variant="outlined"
                        clearable
                        required
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
                    <v-text-field
                        class="mb-2"
                        v-model="confirmPass"
                        :readonly="loading"
                        :rules="[matchPasswords]"
                        :type="showConfirmP ? 'text' : 'password'"
                        :append-icon="showConfirmP ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append="showConfirmP = !showConfirmP"
                        label="Contraseña"
                        variant="outlined"
                        clearable
                        required
                    ></v-text-field>
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-btn
                                :loading="loading"
                                color="green-lighten-1"
                                size="large"
                                type="submit"
                                variant="elevated"
                                block
                            >
                                Crear Cuenta
                            </v-btn>
                        </v-col>
                        
                        <v-col cols="12" md="6">
                            <v-btn
                                :loading="loading"
                                color="red-lighten-1"
                                size="large"
                                type="submit"
                                variant="elevated"
                                block
                                to="/"
                            >
                                Cancelar
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card>
        </v-col>
    </v-row>
</template>
<script>
    export default {
        data: () => ({
            baseUrl: 'http://127.0.0.1:5000/',
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
            phone: '',
            phoneRules: [
                value => {
                    if (value) return true
                    return 'El número de teléfono es requerido.'
                },
                value => {
                    if (/^\d+$/.test(value)) return true
                    return 'El número de teléfono es inválido.'
                },
            ],
            name: '',
            nameRules: [
                value => {
                    if (value) return true
                    return 'El nombre es requerido.'
                },
            ],
            lastName: '',
            lastNRules: [
                value => {
                    if (value) return true
                    return 'El apellido es requerido.'
                },
            ],
            password: null,
            showPassword: false,
            passRules: [
                value => {
                    if (value) return true
                    return 'La contraseña es requerida.'
                },
            ],
            confirmPass: null,
            showConfirmP: false,
            confirmPRules: [
                value => {
                    if (value) return true
                    return 
                },
            ],
            loading: false,
        }),
        methods: {
            matchPasswords() {
                return !this.confirmPass ? 'La confirmación contraseña es requerida.' : (this.password !== this.confirmPass ? 'Las contraseñas no coinciden.' : null);
            },
            async createAccount() {
                try {
                    this.loading = true;
                    const url = this.baseUrl + 'crear_cuenta';
                    let data = {
                            email: this.email,
                            nombres: this.name,
                            apellidos: this.lastName,
                            telefono: this.phone,
                            password: this.password,
                            password2: this.confirmPass // Envía la contraseña al back-end
                        };
                    const request1 = new Request(url, {
                        method: "POST",
                        headers: {
                        'Content-Type': 'application/json' // Ensure you're sending JSON
                        },
                        body: JSON.stringify(data),
                    })

                    const response1 = await fetch(request1);
                    if (response1.status == 200) {
                        alert('Cuenta creada exitosamente');
                        this.$router.push('/');  // Redirigir al inicio de sesión o dashboard
                    } else {
                        const errorData = await response1.json();
                        alert(errorData.message || ' Error al crear la cuenta');
                    }
                    this.loading = false;
                } catch (error) {
                    console.error('Error during registration:', error);
                    alert('Ocurrio un error al intentar crear la cuenta.');
                    this.loading = false;
                }
            },
        },
    }
</script>