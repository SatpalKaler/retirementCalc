<template>
  <v-dialog
    v-model="dialog"
    width="500"
  >
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Support this project</span>
        <v-btn icon="mdi-close" variant="text" @click="$emit('close')"></v-btn>
      </v-card-title>
      <v-card-text>
        <iframe 
          id='kofiframe' 
          src='https://ko-fi.com/satpalkaler' 
          style="border: none; width: 100%; padding: 1px; background: #f9f9f9; height: 550px"
          title='Ko-fi donations'
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'close'])

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script> 