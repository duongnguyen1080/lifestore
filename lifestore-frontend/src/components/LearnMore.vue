<template>
  <div class="learn-more-container">
    <DiamondLoader v-if="loading" />
    <div v-else-if="error">{{ error }}</div>
    <div v-else v-html="authorContent"></div>
  </div>
</template>

<script>
import axios from 'axios';
import DiamondLoader from '@/components/DiamondLoader.vue';

export default {
  name: 'LearnMore',
  components: {
    DiamondLoader
  },
  data() {
    return {
      authorContent: '',  
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchAuthorInfo();
  },
  methods: {
    async fetchAuthorInfo() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_ENDPOINT}/learn-more`, {
          authorInfo: this.$route.params.authorInfo,
          userQuestion: this.$route.params.userQuestion,
          quote: this.$route.params.quote
        });
        this.authorContent = response.data.content;
      } catch (error) {
        console.error('Error fetching author info:', error);
        this.error = error.response?.data?.error || 'An error occurred while fetching the information. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.learn-more-container {
  max-width: 800px;
  margin: 15px 15px;
  padding-top: 50px;
  display: flex;
  position: static;
  justify-content: center;
  align-items: center;
}
</style>