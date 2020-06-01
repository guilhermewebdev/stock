import { Model } from '@vuex-orm/core';

export default class Product extends Model {
    static entity = 'products'

    static fields(){
        return {
            pk: this.attr(null),
            name: this.attr(''),
            description: this.attr(''),
            brand: this.attr(''),
            bar_code: this.attr(''),
            category: this.attr(''),
            registration: this.attr(null),
            amount: this.attr(0),
        }
    }
}