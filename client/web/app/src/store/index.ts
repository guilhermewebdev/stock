import Vue from 'vue'
import Vuex from 'vuex'
import app from '@/sdk'

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
  }
})
