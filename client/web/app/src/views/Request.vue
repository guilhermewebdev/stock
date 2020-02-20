<template>
    <v-container>
        <v-row>
            <v-card
                tile
                right
                class="
                    col-12
                    col-xs-10
                    col-sm-8
                    col-md-7
                    col-lg-5
                    col-xg-4
                    mx-auto
                "
            >
                <v-list-item two-line>
                <v-list-item-content>
                    <v-list-item-title class="headline mb-1">Solicitar produto</v-list-item-title>
                    <v-list-item-subtitle>Preencha o formulário com as informações dos produtos que deseja</v-list-item-subtitle>
                </v-list-item-content>
                </v-list-item>
                <v-form>
                    <v-container>
                        <v-row>
                            <v-col>
                                <v-text-field></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-form>

                <v-card-actions>
                    <v-btn
                        color="primary"
                    >Solicitar</v-btn>
                    <v-btn
                        text
                        color="primary"
                    >Cancelar</v-btn>                    
                </v-card-actions>
            </v-card>
        </v-row>
    </v-container>    
</template>
<script lang="ts">
import Vue from 'vue'
export default {

}
</script>