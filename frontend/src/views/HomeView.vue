<template>
  <v-row>
    <h3>
      <strong>{{ currentUser }}</strong> Profile
    </h3>
  </v-row>
</template>

<script lang="ts">
export default {
  name: "HomeView",
  computed: {
    currentUser(): any {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
  },
};
</script>
