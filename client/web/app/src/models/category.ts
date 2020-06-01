import { Model } from '@vuex-orm/core';

export default class Category extends Model {
    static entity = 'categories'

    static fields() {
        return {
            pk: this.attr(''),
            name: this.attr(''),
            reference: this.attr(''),
            minimum: this.attr(0),
            registration: this.attr(null),
            amount: this.attr(null),
        }
    }
}

