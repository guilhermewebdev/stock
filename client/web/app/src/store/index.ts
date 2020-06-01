import Vue from 'vue'
import Vuex from 'vuex'
import app from '@/sdk'
import VuexORM from "@vuex-orm/core";
import VuexORMAxios from "@vuex-orm/plugin-axios";
import connect from '@/connect';
import { Product } from '@/models';

VuexORM.use(VuexORMAxios, { axios: connect });

const database = new VuexORM.Database();

database.register(Product);

export const plugins = [VuexORM.install(database)];

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isAuthenticated: false,
    loading: false,
  },
  mutations: {
    setAuth(state, playload){
      state.isAuthenticated = playload;
    },
    setLoading(state, playload){
      state.loading = playload
    }
  },
  actions: {
    checkAuth(context){
      app.sessions.checkAuth()
        .then(() => context.commit('setAuth', true))
    },
    toggleLoading(context){
      context.commit('setLoading', !context.state.loading)
    }
  },
  modules: {
  },
  plugins
})
