<script setup lang="ts">
import userService from "@/services/user.service";
import { Form, Field } from "vee-validate";
import * as yup from "yup";

defineProps<{
  img_data: any;
}>();
</script>

<script lang="ts">
export default {
  name: "ImageView",
  data() {
    const schema = yup.object().shape({
      message: yup.string().required("Message is required"),
    });

    return {
      i_liked_computed: this.img_data.i_liked,
      likes_computed: this.img_data.like_count,
      comments_computed: this.img_data.comments,
      comment_count_computed: this.img_data.comment_count,
      loading: false,
      new_comment: "",
      schema,
    };
  },
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
    isAnalysed(): boolean {
      return (
        this.isAdmin &&
        (!this.img_data.analysed_by || this.img_data.analysed_by == "")
      );
    },
  },
  methods: {
    changeLike() {
      this.i_liked_computed = !this.i_liked_computed;

      if (this.i_liked_computed) {
        userService.reactToPost(this.img_data._id);
        this.likes_computed++;
      } else {
        userService.unreactToPost(this.img_data._id);
        this.likes_computed--;
      }
    },
    sendComment(data: any, { resetForm }: any) {
      this.loading = true;
      if (data.message) {
        userService
          .addComment(this.img_data._id, data.message)
          .then(() => {
            this.comments_computed.push({
              username: this.currentUser.username,
              message: data.message,
            });
            this.comment_count_computed++;

            this.loading = false;
            resetForm();
          })
          .catch(() => {
            this.loading = false;
          });
      }
    },
    denyHandler() {
      userService.denyPending(this.img_data._id).then(() => {
        this.$router.go(0);
      });
    },
    approveHandler() {
      userService.approvePending(this.img_data._id).then(() => {
        this.$router.go(0);
      });
    },
  },
};
</script>

<template>
  <div class="post-wrapper">
    <div>
      <button v-if="isAnalysed" @click.prevent="denyHandler" class="deny-btn">
        <span>Deny</span>
      </button>
      <button
        v-if="isAnalysed"
        @click.prevent="approveHandler"
        class="approve-btn"
      >
        <span>Approve</span>
      </button>
      <h2>{{ img_data.title }}</h2>
    </div>
    <div>
      <img :src="img_data.image_uri" />
    </div>
    <hr />
    <div class="options">
      <a
        class="like"
        :class="i_liked_computed ? 'active' : ''"
        @click.prevent="changeLike"
        >👍&nbsp;<span class="counter">{{ likes_computed }}</span></a
      >
      <a class="comments-counter">
        <span class="counter">{{ comment_count_computed }}</span
        >&nbsp;💬</a
      >
    </div>
    <div class="comments">
      <div v-for="comment in img_data.comments" class="comment" :key="comment">
        <div>
          <b class="username">{{ comment.username }}:</b>
          {{ comment.message }}
        </div>
        <hr />
      </div>
      <div class="new-comment">
        <Form @submit="sendComment">
          <Field name="message" type="textarea" /><br />
          <button :disabled="loading">
            <span class="btn-comment">Submit</span>
          </button>
        </Form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-wrapper {
  background-color: var(--color-background-mute);
}

.post-wrapper h2 {
  text-align: center;
  color: var(--color-heading);
}

.post-wrapper img {
  width: 100%;
  height: auto;
  object-fit: contain;
  max-height: 600px;
}

.btn-comment {
  float: right;
}

hr {
  border-color: var(--color-border);
}

.deny-btn,
.approve-btn {
  z-index: 10;
  margin: 5px;
  cursor: pointer;
  display: inline-block;
  border: 2px;
  border-style: solid;
  border-radius: 5px;
  padding: 5px;
}

.deny-btn {
  float: left;

  color: rgb(185, 15, 15);
  background-color: var(--color-background-mute);
}

.approve-btn {
  float: right;

  color: var(--color-text-link);
  background-color: var(--color-background-mute);
}

.options a {
  padding: 5px;
  cursor: pointer;
}

a.like {
  color: transparent;
  font-size: 25px;
  text-shadow: 0 0 0 gray;
}

a.like.active {
  color: white;
  font-size: 25px;
}

a.comments-counter {
  float: right;
  color: white;
  font-size: 19px;
}

a .counter {
  font-size: 20px;
}

.comments {
  width: calc(100% - 20px);
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 5px;
}

.comments .username {
  color: var(--color-text-link);
}

.new-comment input {
  width: 100%;
  border-radius: 5px;
}

.new-comment form {
  text-align: right;
}

.new-comment button {
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
