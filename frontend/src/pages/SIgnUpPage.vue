<template>
    <div class="h1">
      {{ title }}
    </div>
    <form @submit.prevent="handleSubmit" novalidate>
      <div>
        <label for="name">Name</label>
        <input id="name" type="text" v-model="name" required/>
      </div>

      <div>
        <label for="email">Email</label>
        <input id="email" type="email"  v-model="email" required/>
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password"id="password" v-model="password" required/>
      </div>

      <button type="submit" >Sign Up</button>

      <div v-if="apiError" class="api-error">
        <p>{{apiError}}</p>
      </div>
    </form>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Sign Up",
              }
          }
      })
  </script>
  
  <style scoped>
  </style>
  