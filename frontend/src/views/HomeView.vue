<template>
  <div>
    <div v-for="img in posts" :key="img">
      {{ img }}
    </div>
    <h3>
      <strong>{{ currentUser }}</strong> Profile
    </h3>
  </div>
</template>

<script setup lang="ts">
import userService from "@/services/user.service";
</script>

<script lang="ts">
export default {
  name: "HomeView",
  computed: {
    currentUser(): any {
      return this.$store.state.auth.user;
    },
    posts() {
      return [];
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }

    this.posts = userService.getApprovedPosts();
  },
};
</script>
