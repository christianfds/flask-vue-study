<template>
  <div>
    <Form @submit="handleSubmit">
      <label>Image title: </label>
      <Field name="title" type="text" />
      <label for="file">file</label>
      <Field name="file" type="file" />
      <button :disabled="loading">
        <span v-show="loading" class="spinner-border spinner-border-sm"></span>
        <span>Enviar</span>
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
import userService from "@/services/user.service";
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
      title: yup.string().required("Title is required!"),
      file: yup.mixed().required("File is required"),
    });
    return {
      loading: false,
      message: "",
      schema,
    };
  },
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
  methods: {
    async handleSubmit(data: any) {
      this.loading = true;

      function toBase64(file: any) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => resolve(reader.result);
          reader.onerror = (error) => reject(error);
        });
      }

      let send_data = {
        title: data.title,
        file: {
          data: await toBase64(data.file[0]),
        },
      };

      userService.postImage(send_data).then(
        () => {
          this.$router.push("/");
        },
        (error) => {
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

<style></style>
