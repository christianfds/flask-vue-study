<template>
  <div>
    <Form @submit="handleLogin">
      <div class="row-thing">
        <label>Username: </label> <Field name="username" type="text" />
      </div>
      <div class="row-thing">
        <label for="password">Password: </label>
        <Field name="password" type="password" class="form-control" />
      </div>

      <button :disabled="loading">
        <span v-show="loading" class="spinner-border spinner-border-sm"></span>
        <span>Login</span>
      </button>
      <div class="form-group">
        <div v-if="message" class="alert alert-danger" role="alert">
          {{ message }}
        </div>
      </div>
    </Form>
  </div>
</template>

<script setup lang="ts">
import { Form, Field } from "vee-validate";
import * as yup from "yup";
</script>
<script lang="ts">
export default {
  name: "LoginView",
  components: {
    Form,
    Field,
    // ErrorMessage,
  },
  data() {
    const schema = yup.object().shape({
      username: yup.string().required("Username is required!"),
      password: yup.string().required("Password is required!"),
    });
    return {
      loading: false,
      message: "",
      schema,
    };
  },
  computed: {
    loggedIn(): any {
      return this.$store?.state?.auth?.status?.loggedIn || false;
    },
  },
  created() {
    if (this.loggedIn) {
      this.$router.push("/");
    }
  },
  methods: {
    handleLogin(user: any) {
      this.loading = true;
      this.$store.dispatch("auth/login", user).then(
        () => {
          this.$router.push("/");
        },
        (error: any) => {
          this.loading = false;
          this.message =
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString();
        }
      );
    },
  },
};
</script>

<style scoped>
form {
  background-color: var(--color-background-mute);
  padding: 50px;
  border-radius: 20px;
  min-width: 350px;
  width: 25vw;
  text-align: right;
  font-weight: bolder;
}

form .row-thing {
  width: 100%;
  display: flex;
  margin-bottom: 10px;
  text-align: left;
}

form .row-thing label {
  width: 20%;
}
form .row-thing input {
  width: 80%;
}

form button {
  cursor: pointer;
  display: inline-block;
  color: var(--color-text-link);
  background-color: var(--color-background-mute);
  border: 2px;
  border-style: solid;
  border-radius: 5px;
  padding: 5px;
}
</style>
