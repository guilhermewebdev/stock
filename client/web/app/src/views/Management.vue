<template>
  <v-container fluid v-resize="resize" style="height: calc(100vh - 60px);" class="py-0">
    <v-row class="h-100" justify="start" align="stretch" style="height: calc(100vh - 60px);">
      <v-card
        tile
        class="col-md-3 h-100 px-0 d-flex position-relative flex-column py-0"
        style="height: calc(100vh - 60px);"
      >
        <v-toolbar class="w-100 flex-grow-0" tile dense>
          <v-toolbar-title>Categorias</v-toolbar-title>

          <v-spacer></v-spacer>

          <CreateCategory v-on:created="refresh" />
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-toolbar>
        <v-list class="flex-grow-1 overflow-y-auto">
          <template v-for="(item) in categories">
            <v-list-item :to="`/management/cat/${item.pk}/`" :key="item.pk">
              <v-list-item-avatar>
                <v-progress-circular
                  :size="40"
                  :rotate="270"
                  :value="(item.amount/item.minimum)*50"
                  :color="item.amount === 0 ?
                   'error' : item.amount < item.minimum ?
                    'warning' : 'success'"
                >{{ item.reference }}</v-progress-circular>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="item.name"></v-list-item-title>
                <v-list-item-subtitle>
                  <span>
                    <span>Disponível: {{item.amount}}</span>
                    <span class="ml-5">Mínimo: {{item.minimum}}</span>
                  </span>
                  <v-spacer />
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-card>
      <v-col
        md="9"
        class="px-0 py-0 d-flex position-relative h-100 flex-column"
        style="height: calc(100vh - 60px);"
        v-if="$route.params.cat"
      >
        <v-expansion-panels class="flex-grow-0 w-100" focusable hover tile>
          <v-expansion-panel>
            <v-expansion-panel-header>{{ selected.name }}</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-progress-linear
                :color="selected.amount === 0 ?
                   'error' : selected.amount < selected.minimum ?
                    'warning' : 'success'"
                :value="(selected.amount/selected.minimum)*50"
              ></v-progress-linear>

              <v-row justify="space-between" dense>
                <v-col cols="3">
                  <span>Quantidade Disponível: {{ selected.amount }}</span>
                </v-col>
                <v-col cols="3">
                  <span>Quantidade Mínima: {{ selected.minimum }}</span>
                </v-col>
                <v-col cols="3">
                  <span>Data de Cadastro: {{ new Date(selected.registration).toLocaleString('pt-BR', { timeZone: 'UTC' }) }}</span>
                </v-col>
              </v-row>
              <v-row justify="end">
                <v-col md="2" class="d-flex justify-end">
                  <v-dialog v-model="deletionCatDialog" persistent max-width="290">
                    <template v-slot:activator="{ on }">
                      <v-btn v-on="on" text>Deletar</v-btn>
                    </template>
                    <v-card>
                      <v-card-title class="headline">Deletar {{ selected.name }}</v-card-title>
                      <v-card-text>Você tem certeza que deseja apagar permanentemente a categoria {{ selected.name }}, com {{ selected.amount }} items?</v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="deleteCategory">Deletar</v-btn>
                        <v-btn color="primary" text @click="deletionCatDialog = false;">Cancelar</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <create-category v-on:created="refresh" toUpdate :category="selected" />
                </v-col>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-flex class="overflow-y-auto">
          <v-data-table
            :headers="[
              { text: 'Marca', value: 'brand' },
              { text: 'Quantidade', value: 'amount', align: 'center' },
              { text: 'Data do cadastro', value: 'registration', align: 'center' },
              { text: 'Código', value: 'bar_code' },
              { text: 'Ações', value: 'actions', sortable: false, align: 'center' }
            ]"
            :fixed-header="true"
            :items="selected.products.map((item) => {
            return {
              ...item,
              registration: new Date(item.registration).toLocaleString('pt-BR', { timeZone: 'UTC' })
            };
          })"
            item-key="name"
            class="flex-grow-1 overflow-y-auto d-flex flex-column position-relative"
            :search="searchProduct"
            locale="pt-BR"
          >
            <template v-slot:top>
              <v-container class="flex-grow-0">
                <v-row>
                  <v-col md="4">
                    <v-text-field
                      prepend-inner-icon="mdi-magnify"
                      clearable
                      label="Buscar"
                      autocomplete="off"
                      v-model="searchProduct"
                    />
                  </v-col>
                  <v-col md="2" class="d-flex justify-center align-center">
                    <create-product v-on:created="refresh" />
                  </v-col>
                </v-row>
              </v-container>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn :key="item.pk" color="primary" icon>
                <v-icon small @click="dialogRemoval(item)">mdi-minus-box</v-icon>
              </v-btn>
              <create-product :key="item.pk" toUpdate @created="refresh" :product="item" />
              <v-btn :key="item.pk" color="primary" icon>
                <v-icon small @click="dialogDelete(item)">mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-flex>
        <v-dialog v-model="deletionDialog" persistent max-width="290">
          <v-card>
            <v-card-title class="headline">Deletar Produto</v-card-title>
            <v-card-text>Você tem certeza que deseja apagar permanentemente o produto {{ selected.name }}, da marca {{ deletionItem.brand }} com {{ deletionItem.amount }} items e o código {{ deletionItem.bar_code }}?</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="deleteProduct">Deletar</v-btn>
              <v-btn
                color="primary"
                text
                @click="deletionDialog = false; deletionItem = {};"
              >Cancelar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="removalDialog" persistent max-width="290">
          <v-card>
            <v-card-title class="headline">Remover do Estoque</v-card-title>
            <v-card-text>
              <v-row>
                <v-text-field
                  class="col-12"
                  label="Quantidade"
                  :min="1"
                  :max="removalItem.amount"
                  type="number"
                  v-model="amoutRemoval"
                  persistent-hint
                  :rules="[
                    v => v <= removalItem.amount || `Existem apenas ${removalItem.amount} itens no estoque`,
                    v => v > 0 || 'Informe uma quantidade válida'
                  ]"
                  hint="Informe a quantidade de itens a serem removidos do estoque"
                />
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="removeProduct">Remover</v-btn>
              <v-btn color="primary" text @click="removalDialog = false; removalItem = {};">Cancelar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="editDialog" persistent max-width="290">
          <v-card>
            <v-card-title class="headline">Use Google's location service?</v-card-title>
            <v-card-text>Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click="dialog = false">Disagree</v-btn>
              <v-btn color="primary" text @click="dialog = false">Agree</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import app from "@/sdk";
import CreateCategory from "./CreateCategory.vue";
import CreateProduct from "./CreateProduct.vue";
import connect from "../connect";

export default Vue.extend({
  name: "management",
  data: () => ({
    categories: null,
    height: window.innerHeight - 48,
    searchProduct: "",
    deletionDialog: false,
    deletionCatDialog: false,
    editDialog: false,
    editionItem: {},
    deletionItem: {},
    removalItem: {},
    removalDialog: false,
    amoutRemoval: 1
  }),
  beforeMount() {
    this.refresh();
  },
  computed: {
    selected() {
      return this.categories.filter(
        item => item.pk == this.$route.params.cat
      )[0];
    }
  },
  methods: {
    async refresh() {
      connect.get("/categories/?format=json").then(({ data }) => {
        this.categories = data;
      });
    },
    async resize() {
      this.height = window.innerHeight - 60;
    },
    async dialogDelete(item) {
      this.deletionItem = item;
      this.deletionDialog = true;
    },
    async deleteProduct() {
      connect
        .delete(`/products/${this.deletionItem.pk}/`)
        .then(this.refresh)
        .then(() => (this.deletionItem = {}))
        .then(() => (this.deletionDialog = false));
    },
    async deleteCategory() {
      connect
        .delete(`/categories/${this.selected.pk}/`)
        .then(this.refresh)
        .then(() => this.$router.push("/management/"));
    },
    async dialogRemoval(item) {
      this.removalDialog = true;
      this.removalItem = item;
    },
    async removeProduct() {
      connect.post(`/removals/?format=json`, {
        product: this.removalItem.pk,
        amount: this.amoutRemoval
      }).then(() => {
        this.refresh();
        this.removalDialog = false;
        this.removalItem = {};
      });
    }
  },
  components: {
    CreateCategory,
    CreateProduct
  }
});
</script>
