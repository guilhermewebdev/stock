<template>
    <div style="heigth:100%;">
         <v-navigation-drawer
          permanent
          absolute
          expand-on-hover
          mini-variant
        >
          <v-list>
            <v-list-item class="px-2">
              <v-list-item-avatar>
                <v-avatar :color="createColor">
                    <span class="white--text headline">{{ sdk.sessions.user.username[0].toUpperCase() }}</span>
                </v-avatar>
              </v-list-item-avatar>
            </v-list-item>

            <v-list-item link>
              <v-list-item-content>
                <v-list-item-title class="title">@{{ sdk.sessions.user.username }}</v-list-item-title>
                <v-list-item-subtitle>{{ sdk.sessions.user.email }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>
          <v-list
          >
            <v-list-item link to='/home'>
              <v-list-item-icon>
                <v-icon>mdi-home</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Início</v-list-item-title>
            </v-list-item>
            <v-list-item link to='/requests'>
              <v-list-item-icon>
                <v-icon>mdi-minus-box</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Solicitar</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/management">
              <v-list-item-icon>
                <v-icon>mdi-card-bulleted-settings</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Gerenciar</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/settings">
              <v-list-item-icon>
                <v-icon>mdi-settings</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Configurações</v-list-item-title>
            </v-list-item>
          </v-list>
          <template v-slot:append>
            <v-divider></v-divider>
            <v-list
              nav
              dense
            >          
            <v-list-item link @click="logout">
              <v-list-item-icon>
                <v-icon>mdi-exit-run</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Sair</v-list-item-title>
            </v-list-item>
          </v-list>
          </template>
        </v-navigation-drawer>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'
import app from '../sdk';

export default Vue.extend({
    name: 'navigation',
    data(){
        return {
            sdk: app,
        }
    },
    methods: {
      logout(){
        app.sessions.logout()
        this.$router.push('/')
      }
    },
    computed: {
        createColor(){
            let hexadecimais = '0123456789ABCDEF';
            let cor = '#';
            // Pega um número aleatório no array acima
            for (let i = 0; i < 6; i++) {
            //E concatena à variável cor
                cor += hexadecimais[Math.floor(Math.random() * 16)];
            }
            return cor;
        },        
    },
})
</script>