<script setup lang="ts">
import { RouterLink } from "vue-router";

defineProps<{
  destination: string;
  title: string;
  logout: string;
}>();
</script>

<script lang="ts">
export default {
  methods: {
    logOut() {
      this.$store.dispatch("auth/logout");
      this.$router.push("/login");
    },
  },
};
</script>

<template>
  <div class="header-btn">
    <a v-if="logout == 'true'" @click.prevent="logOut"
      ><span>{{ title }}</span></a
    >
    <RouterLink
      v-if="logout != 'true'"
      :to="{ path: destination }"
      class="header-link"
      ><span>{{ title }}</span></RouterLink
    >
  </div>
</template>

<style>
.header-btn {
  height: 100%;
  width: auto;
  display: inline-flex;
}

.header-btn a {
  display: inline-flex;
  align-items: center;
  padding: 0 1rem;
}
</style>
