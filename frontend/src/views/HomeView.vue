<script setup lang="ts">
import userService from "@/services/user.service";
import Image from "@/components/Image.vue";
</script>

<template>
  <div class="centralize">
    <div v-for="img in posts" :key="img">
      <Image :img_data="img"></Image>
      <!-- {{ img }} -->
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "HomeView",
  data() {
    return {
      posts: [],
    };
  },
  computed: {
    currentUser(): any {
      return (
        this.$store?.state?.auth?.user?.data || this.$store?.state?.auth?.user
      );
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }

    userService.getApprovedPosts().then((response) => {
      this.posts = response.data.data;
    });
  },
};
</script>

<style>
.centralize {
  min-width: 700px;
  max-width: 60vw;
}
</style>
