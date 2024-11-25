<template>
    <v-container>
      <v-card>
        <v-card-title>
          Mantenimiento de Estados
          <v-spacer></v-spacer>
          <v-btn @click="openDialog('add')" color="primary" append-icon="mdi-plus">Agregar</v-btn>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="categories"
          item-value="id"
          class="elevation-1"
          items-per-page-text="Registros por página"
          :items-per-page-options="[{value: 10, title: '10'},
                                    {value: 20, title: '20'},
                                    {value: 30, title: '30'}]"
        >
          <template v-slot:[`item.actions`]="{ item }">
            <v-btn icon @click="openDialog('edit', item)" class="mx-2">
              <v-icon color="green">mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteCategory(item.id)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card>
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span v-if="dialogType === 'add'">Agregar Estado</span>
            <span v-else>Editar Estado</span>
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="form.description"
              label="Descripción"
              required
            ></v-text-field>
            <v-text-field
              v-model="form.capacity"
              label="Capacidad"
              required
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red darken-1" text @click="closeDialog">Cancelar</v-btn>
            <v-btn color="blue darken-1" text @click="saveCategory">Guardar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
</template>

<script>
export default {
  data() {
    return {
      headers: [
        { title: 'ID', key: 'id' },
        { title: 'Descripción', key: 'description' },
        { title: 'Capacidad', key: 'capacity' },
        { title: 'Acciones', align: 'center', key: 'actions', sortable: false },
      ],
      categories: [
        { id: 1, description: 'Denegada', capacity: 0 },
        { id: 2, description: 'Pendiente', capacity: 0 },
      ],
      dialog: false,
      dialogType: 'add',
      form: {
        id: null,
        description: '',
        capacity: 0
      },
    };
  },
  methods: {
    openDialog(type, item = null) {
      this.dialogType = type;
      if (type === 'edit' && item) {
        this.form = { ...item };
      } else {
        this.form = { id: null, description: '', capacity: 0 };
      }
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    saveCategory() {
      if (this.dialogType === 'add') {
        const newId = this.categories.length + 1;
        this.categories.push({ ...this.form, id: newId });
      } else if (this.dialogType === 'edit') {
        const index = this.categories.findIndex(c => c.id === this.form.id);
        if (index !== -1) {
          this.categories.splice(index, 1, { ...this.form });
        }
      }
      this.closeDialog();
    },
    deleteCategory(id) {
      this.categories = this.categories.filter(c => c.id !== id);
    },
    getData() {}
  },
};
</script>

<style scoped>
.elevation-1 {
  margin-top: 20px;
}
</style>