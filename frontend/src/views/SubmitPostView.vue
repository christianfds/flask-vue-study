<template>
  <div>
    <Form @submit="handleSubmit">
      <div class="row-thing">
        <label>Image title: </label> <Field name="title" type="text" />
      </div>
      <div class="row-thing">
        <label id="input_label" for="file_input">{{ upload_file_text }}</label>
        <Field
          id="file_input"
          name="file_input"
          type="file"
          @change="fileChanged"
        />
      </div>
      <button :disabled="loading">
        <span v-show="loading" class="spinner-border spinner-border-sm"></span>
        <span>Submit</span>
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
  },
  data() {
    const schema = yup.object().shape({
      title: yup.string().required("Title is required!"),
      file_input: yup.mixed().required("File is required"),
    });
    return {
      loading: false,
      message: "",
      upload_file_text: " Choose your file ",
      schema,
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
  },
  methods: {
    fileChanged(event: any) {
      this.upload_file_text =
        event?.target?.files[0]?.name || " Choose your file ";
    },
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

      if (!data.title || !data.file_input) {
        this.loading = false;
      }

      let send_data = {
        title: data.title,
        file: {
          data: await toBase64(data.file_input[0]),
        },
      };

      userService.postImage(send_data).then(
        () => {
          this.loading = false;
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

form button,
form #input_label {
  cursor: pointer;
  display: inline-block;
  color: var(--color-text-link);
  background-color: var(--color-background-mute);
  border: 2px;
  border-style: solid;
  border-radius: 5px;
  padding: 5px;
}

form #input_label {
  color: rgb(97, 97, 255);
  width: 100%;
  text-align: center;
}

#file_input {
  display: none;
}
</style>
