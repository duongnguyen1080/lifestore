import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css'

import mdiVue from 'mdi-vue/v3'
import * as mdijs from '@mdi/js'

import mixpanel from "mixpanel-browser";
mixpanel.init("c8ecaa35478b649afbb6b6366339fedf", {
  debug: true,
  track_pageview: true,
  persistence: "localStorage",
});

const app = createApp(App)

app.use(router)

app.use(mdiVue, {
  icons: mdijs
})

app.mount('#app')