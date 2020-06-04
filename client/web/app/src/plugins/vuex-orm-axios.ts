import { Model } from '@vuex-orm/core';
import connect from '@/connect';

export default () => {
      Model.setAxios(connect);
}