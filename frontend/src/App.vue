<script setup lang="ts">
import { RouterView } from "vue-router";
import Header from "@/components/Header.vue";
</script>

<template>
  <Header />
  <div id="body">
    <RouterView />
  </div>
  <!-- <notifications group="general" /> -->
</template>

<style>
@import "@/assets/base.css";

#app {
  margin: 0 auto;
  padding: 0;

  font-weight: normal;
}

#body {
  display: flex;
  place-items: center;
  justify-content: center;
  min-height: calc(100vh - 50px);
  overflow-x: hidden;
}
</style>
