<script setup lang="ts">
import { RouterLink } from "vue-router";
import HeaderButton from "@/components/HeaderButton.vue";
</script>

<script lang="ts">
export default {
  name: "HeaderView",
  computed: {
    currentUser(): any {
      return (
        this.$store?.state?.auth?.user?.data || this.$store?.state?.auth?.user
      );
    },
    isAdmin(): boolean {
      if (this?.currentUser?.roles) {
        return this.currentUser.roles.indexOf("admin") > 0;
      }
      return false;
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
  },
};
</script>

<template>
  <header>
    <!-- <HelloWorld msg="You did it!" /> -->
    <nav>
      <HeaderButton
        logout="false"
        destination="#"
        title="Gallery"
        class="align-left"
      ></HeaderButton>
      <HeaderButton logout="false" destination="/" title="Home"></HeaderButton>
      <HeaderButton
        logout="false"
        destination="/upload"
        title="Upload new image"
      ></HeaderButton>
      <HeaderButton
        v-if="isAdmin"
        logout="false"
        destination="/pending"
        title="Pending images"
      ></HeaderButton>
      <HeaderButton
        v-if="currentUser"
        logout="true"
        destination="#"
        title="Logout"
        class="align-right"
      ></HeaderButton>
    </nav>
  </header>
</template>

<style>
header {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  line-height: 1.5;
  height: 50px;
  min-height: 20px;
  max-height: auto;
}

.align-left {
  float: left;
}

.align-right {
  float: right;
}

a,
.green {
  text-decoration: none;
  color: var(--color-text-link);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

nav {
  width: 100%;
  height: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 0;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a:first-of-type {
  border: 0;
}
</style>
