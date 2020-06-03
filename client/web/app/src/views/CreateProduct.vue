<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" dark v-on="on">Novo Produto</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Novo Produto</span>
      </v-card-title>
      <v-form autocomplete="off" ref="form">
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="8" md="8">
                <v-text-field
                  label="Marca *"
                  :rules="[rules.required, errors.brand]"
                  v-model="form.brand"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="4" md="4">
                <v-text-field
                  label="Quantidade *"
                  :rules="[rules.required, errors.amount]"
                  v-model="form.amount"
                  type="number"
                  min="0"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="12" md="12">
                <v-text-field
                  label="Código de barras *"
                  :rules="[rules.required, errors.bar_code, v => /^[0-9]{1,30}$/g.test(v) || 'Digite um código válido']"
                  v-model="form.bar_code"
                  required
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
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import Vue from "vue";
import { Product } from "../models";
import connect from "../connect";
export default Vue.extend({
  name: "CreateProduct",
  data: vm => ({
    dialog: false,
    form: {
      category: vm.$route.params.cat,
      brand: null,
      amount: null,
      bar_code: null
    },
    rules: {
      required: v => !!v || "Este campo é obrigatório"
    },
    errors: {
      brand: true,
      amount: true,
      bar_code: true
    }
  }),
  methods: {
    async submit() {
      if (this.$refs.form.validate()) {
        connect
          .post("/products/?format=json", this.$data.form)
          .then(response => {
            this.$refs.form.reset();
            this.$emit("created", response);
          })
          .catch(({ response }) => {
            if (response) {
              for (let index in response.data) {
                this.errors[index] = response.data[index][0];
              }
              this.$refs.form.validate();
              this.errors = {
                brand: true,
                amount: true,
                bar_code: true
              };
            }
          });
      }
    }
  }
});
</script>