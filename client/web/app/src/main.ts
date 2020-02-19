import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import app from '@/sdk';

Vue.config.productionTip = false

app.sessions.addObserver((sessions:any) => {
  if(sessions.isAuthenticated !== undefined) store.commit('setAuth', sessions.isAuthenticated)
})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App),
  beforeMount(){
    app.mount()
  }
}).$mount('#app')
