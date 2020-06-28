import vuetify from './plugins/vuetify';
import Vue from "vue";
import App from "./App.vue";
import { Datetime } from "vue-datetime";
Vue.use(Datetime);
Vue.use(vuetify);
Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
