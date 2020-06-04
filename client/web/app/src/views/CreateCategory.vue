<template>
  <v-dialog v-model="dialog" persistent max-width="600px">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-form @keypress.native.enter="submit" autocomplete='off' ref="form">
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
                  hint="Informe o nome da categoria"
                  persistent-hint
                  required
                  :rules="[v => errors.name, rules.required]"
                  v-model="form.name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Referência *"
                  hint="Informe uma identificação única para esta categoria"
                  persistent-hint
                  :rules="[v => errors.reference, rules.required, v => v.length <= 4 || 'Máximo de 4 caractéres']"
                  required
                  counter="4"
                  v-model="form.reference"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  label="Quantidade mínima *"
                  hint="Informe a quantidade mínima de estoque"
                  persistent-hint
                  required
                  type="number"
                  min="0"
                  :rules="[
                    v => errors.minimum,
                    rules.required,
                  ]"
                  v-model="form.minimum"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>* Indica campos obrigatórios</small>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="reset">Limpar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Fechar</v-btn>
          <v-btn color="primary" @click="submit">Salvar</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>
<script lang="ts">
import Vue from "vue";
import connect from "../connect";
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
      name: true,
      reference: true,
      minimum: true
    },
    rules: {
      required: v => !!v || "Este campo é obrigatório"
    }
  }),
  methods: {
    async reset() {
      this.$refs.form.reset();
    },
    async submit() {
      if (this.$refs.form.validate()) {
        connect
          .post("/categories/", this.form)
          .then(response => {
            this.$refs.form.reset();
            this.$emit("created", response.data);
          })
          .catch(response => {
            for (let index in response.data) {
              this.errors[index] = response.data[index][0];
            }
            this.$refs.form.validate();
            this.errors = {
              name: true,
              reference: true,
              minimum: true
            };
          });
      }
    }
  }
});
</script>