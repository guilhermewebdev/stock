<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" icon v-if="!!toUpdate" v-on="on">
        <v-icon small @click="editDialog = true">mdi-pencil</v-icon>
      </v-btn>
      <v-btn color="primary" v-else v-on="on">Novo Produto</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">Novo Produto</span>
      </v-card-title>
      <v-form autocomplete="off" ref="form" @keypress.native.enter="submit">
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
          <v-btn color="primary" text @click="$refs.form.reset()">Limpar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Fechar</v-btn>
          <v-btn color="primary" @click="submit">Salvar</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import Vue from "vue";
import connect from "../connect";

export default Vue.extend({
  name: "CreateProduct",
  props: {
    toUpdate: {
      type: Boolean,
      required: false,
      default: false
    },
    product: {
      type: Object,
      required: false
    }
  },
  data: vm => ({
    dialog: false,
    form: {
      brand: vm.toUpdate ? vm.product.brand : null,
      amount: vm.toUpdate ? vm.product.amount : null,
      bar_code: vm.toUpdate ? vm.product.bar_code : null
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
        connect[this.$props.toUpdate ? "put" : "post"](
          `/products/${
            this.$props.toUpdate ? this.$props.product.pk + "/" : ""
          }`,
          {
            category: this.$route.params.cat,
            ...this.$data.form
          }
        )
          .then(({ data }) => {
            this.$emit("created", data);
            this.$props.toUpdate
              ? (this.$data.dialog = false)
              : this.$refs.form.reset();
          })
          .catch(({ response }) => {
            if (response) {
              for (let index in response.data) {
                this.$data.errors[index] = response.data[index][0];
              }
              this.$refs.form.validate();
              this.$data.errors = {
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