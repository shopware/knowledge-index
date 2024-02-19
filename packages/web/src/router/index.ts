import { createRouter, createWebHashHistory } from 'vue-router'
import HomePage from '../page/HomePage.vue'
import CollectionPage from '../page/CollectionPage.vue'
import CollectionsPage from '../page/CollectionsPage.vue'
import StoragePage from '../page/StoragePage.vue'
import CachePage from '../page/CachePage.vue'
import HealthcheckPage from '../page/HealthcheckPage.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/collection/:collection',
      name: 'collection',
      component: CollectionPage
    },
    {
      path: '/collections',
      name: 'collections',
      component: CollectionsPage
    },
    {
      path: '/storage',
      name: 'storage',
      component: StoragePage
    },
    {
      path: '/cache',
      name: 'cache',
      component: CachePage
    },
    {
      path: '/healthcheck',
      name: 'healthcheck',
      component: HealthcheckPage
    },
  ]
})

export default router
