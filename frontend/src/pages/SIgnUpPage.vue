<template>
    <div class="h1">
      {{ title }}
    </div>
    <form novalidate>
      <div>
        <label for="name">Name</label>
        <input id="name" type="text" v-model="name" required/>
      </div>
      <div>
        <label for="date_of_birth">Date of Birth</label>
        <input id="date_of_birth" type="date" v-model="date_of_birth" required /> 
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

  
    </form>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Sign Up",
                  name: '',
                  date_of_birth: '',
                  email: '',
                  password: '',


              }
          }
      })
  </script>
  
  <style scoped>
  </style>
  