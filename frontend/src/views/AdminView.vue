<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
      <div class="flex flex-col gap-4">
        <CardCategory
          v-for="category in categories"
          :key="category.title"
          :title="category.title"
          :items="category.items"
        />
      </div>
    </div>
    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import CardCategory from '@/components/common/CardCategory.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'

export default {
  name: 'AdminView',
  components: { BasePage, BaseBreadcrumbs, CardCategory, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Admin', to: '/' }],
      categories: [
        {
          title: 'Zugriff',
          items: [
            { icon: 'permission', label: 'Rollen & Rechte', to: '/admin/roles' },
            { icon: 'people', label: 'Nutzer', to: '/admin/users' },
          ],
        },
        {
          title: 'Inhalte',
          items: [
            { icon: 'country_flags/switzerland', label: 'Über mich', to: '/admin/about' },
            { icon: 'integrity', label: 'Ethos', to: '/admin/ethos' },
            { icon: 'cover-letter', label: 'Lebenslauf', to: '/admin/cv' },
            { icon: 'destination', label: 'Länder', to: '/admin/countries' },
            { icon: 'social-media', label: 'Medien', to: '/admin/media' },
          ],
        },
        {
          title: 'Rechtliches',
          items: [
            { icon: 'calendar_and_date/verified', label: 'Impressum', to: '/admin/impressum' },
            { icon: 'privacy-policy', label: 'Datenschutzerklärung', to: '/admin/privacy' },
            { icon: 'breakfast/cookies', label: 'Cookierichtlinien', to: '/admin/cookies' },
            { icon: 'calendar_and_date/agreement', label: 'Nutzungsrichtlinien', to: '/admin/terms' },
            { icon: 'law_and_justice/attorney', label: 'Haftungsausschluss', to: '/admin/disclaimer' },
          ],
        },
      ],
    }
  },
}
</script>
