<script setup lang="ts">
import HomeView from './views/HomeView.vue'
import { NavBar } from 'vant'
import { Button } from 'vant'
</script>

<template lang="pug">
div(ref='app')
  NavBar(
    title='语音合成系统'
  )
  HomeView
</template>

<style>
html {
  height: 100%;
  background-color: white;
}
#app {
  display: block;
  margin: 0;
  padding: 0;
  background-color: white;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
