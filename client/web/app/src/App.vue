<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <a to="/" class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://caio.odo.br/static/imagens/logo/logo-desenho.png"
          transition="scale-transition"
          width="40"
        />
        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://caio.odo.br/static/imagens/logo/logo-maior-1080_Kq4TX1E.png"
          width="150"
        />
      </a>
      <v-progress-linear indeterminate color="#ADFF2F" bottom fixed v-show="loading"></v-progress-linear>
    </v-app-bar>
    <navigation v-if="authenticated"></navigation>
    <v-content v-resize="resize" style="height: calc(100vh - 64px);">
      <router-view style="height: 100%"></router-view>
    </v-content>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import Navigation from "@/components/Navigation";
export default Vue.extend({
  name: "App",
  components: {
    Navigation
  },
  computed: {
    loading() {
      return this.$store.state.loading;
    },
    authenticated() {
      return this.$store.state.isAuthenticated;
    }
  },
  data: () => ({
    height: window.innerHeight - 64
  }),
  // mounted() {
  //   if (!this.$store.state.isAuthenticated) this.$router.push("/");
  // },
  // beforeUpdate() {
  //   if (!this.$store.state.isAuthenticated) this.$router.push("/");
  // },
  methods: {
    resize() {
      this.height = window.innerHeight - 64;
    }
  }
});
</script>
