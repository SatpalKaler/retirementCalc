<template>
  <v-app>
    <v-main>
      <Analytics />
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { Analytics } from "@vercel/analytics/react"
</script>
