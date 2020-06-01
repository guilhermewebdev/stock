<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-form
        ref="form"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Nova Categoria</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="12" md="12">
                <v-text-field
                  label="Nome *"
                  :hint="!!errors.name ? erros.name : 'Informe o nome da categoria'"
                  persistent-hint
                  required
                  :error='!!errors.name'
                  v-model="form.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Referência *"
                  :hint="errros.reference ? errors.reference : 'Informe uma identificação única para esta categoria'"
                  persistent-hint
                  required
                  :error='!!errors.reference'
                  v-model="form.reference"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Quantidade mínima *"
                  :hint="errors.minumum ? errors.minimum : 'Informe a quantidade mínima de estoque'"
                  persistent-hint
                  required
                  type="number"
                  min="0"
                  :error='!!errors.minimum'
                  v-model="form.minimum"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>* Indica campos obrigatórios</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" text @click="submit">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>
<script lang="ts">
import Vue from "vue";
import { Category } from "../models";

export default Vue.extend({
  name: "CrateCategory",
  data: () => ({
    dialog: false,
    form: {
      name: null,
      reference: null,
      minimum: 0
    },
    errors: {
        name: null,
        reference: null,
        minimum: null,
    }
  }),
  methods: {
    async submit() {
      Category.api()
        .post("/categories/", this.form)
        .then(({ response }) => {
            this.$refs.form.reset();
            this.$emit('created', response);
        })
        // .catch(({ response }) => {
            
        // });
    }
  }
});
</script>