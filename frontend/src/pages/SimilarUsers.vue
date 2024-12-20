<template>
    <div class="h3">
      {{ title }}
    </div>
</template>
  
<script lang="ts">
    import { defineComponent } from "vue";
    const baseUrl = 'http://127.0.0.1:8000'

    export default defineComponent({
        data() {
            return {
                title: "Similar Users",
                similar_users: []
            }
        },
        methods: {
            async getSimilarUsers() {
                try {
                    const response = await fetch(`${baseUrl}/similar-users/`, {
                        method: "GET",
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });
                    if (!response.ok) throw new Error("Failed to fetch similar users");
                    
                    const similarUsers  = await response.json();
                    
                    this.similar_users = similarUsers;
                    if (response.status===404){
                        alert(similarUsers.message);
                    }
                } catch (error) {
                    console.error("There was an error:", error);
                }
            }
        }
    })
</script>

<style scoped>
</style>
