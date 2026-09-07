<script setup>
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import { icons } from '@/assets/icons.js'
import { mediaGroups } from '@/data/media.js'

const breadcrumbs = [{ label: 'Medien', to: '/' }]
</script>

<template>
  <Page active-navigation="media">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex">
      <div class="mx-auto w-150">
        <ul
          v-for="group in mediaGroups"
          :key="group.title"
          class="list bg-base-100 rounded-box shadow-none border-wntrs-gray border-solid border-1 mt-16"
        >
          <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">{{ group.title }}</li>
          <li v-for="item in group.items" :key="item.url" class="list-row">
            <div>
              <img class="size-10" :alt="item.platform" :src="icons[item.icon]" />
            </div>
            <div class="flex">
              <div class="my-auto">{{ item.name }}</div>
            </div>
            <a :href="item.url" class="btn btn-square btn-ghost">
              <img class="size-[1.2em]" alt="open" :src="icons['share-square']" />
            </a>
          </li>
        </ul>
      </div>
    </div>
  </Page>
</template>
