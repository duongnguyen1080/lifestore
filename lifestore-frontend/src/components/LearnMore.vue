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
    this.initializeLearnMore();
  },
  watch: {
    // Watch for route query changes
    '$route.query': {
      handler: 'initializeLearnMore',
      immediate: true
    }
  },
  methods: {
    initializeLearnMore() {
      // Reset state
      this.loading = true;
      this.error = null;
      this.authorContent = '';

      // Validate required query parameters
      const requiredParams = ['quote', 'philosopher', 'source', 'userQuestion'];
      const missingParams = requiredParams.filter(param => !this.$route.query[param]);
      
      if (missingParams.length > 0) {
        this.error = `Missing required parameters: ${missingParams.join(', ')}`;
        this.loading = false;
        return;
      }
      
      this.fetchAuthorInfo();
    },
    async fetchAuthorInfo() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_ENDPOINT}/learn-more`, {
          quote: this.$route.query.quote || '',
          philosopher: this.$route.query.philosopher || '',
          source: this.$route.query.source || '',
          year: this.$route.query.year === '-' ? '' : (this.$route.query.year || ''),
          userQuestion: this.$route.query.userQuestion || ''
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