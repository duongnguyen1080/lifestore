<template>
    <div class="home">
    <QueryCard 
      v-if="!quotes.length"
      :isLoading="isLoading"
      :error="error"
      :question="question"
      @submit="handleSubmit"
    />
    <ShowQuote 
      v-else
      :quotes="quotes"
      :userQuestion="question"
      @editQuery="resetQuery"
    />
  </div>
  </template>
  
  <script>
  import axios from 'axios'
  import QueryCard from '@/components/QueryCard.vue'
  import ShowQuote from '@/components/ShowQuote.vue'
  
  export default {
    name: 'AppHome',
    components: {
      QueryCard,
      ShowQuote
    },
    data() {
      return {
        question: '',
        quotes: [],
        isLoading: false,
        error: ''
      }
    },
    created() {
      console.log('AppHome created:', {
        route: this.$route.name,
        quotes: this.quotes,
        question: this.question
      });
      if (this.$router._savedState) {
        console.log('Restoring state:', this.$router._savedState);
        this.quotes = this.$router._savedState.quotes;
        this.question = this.$router._savedState.question;
        this.$router._savedState = null;
      }
    },
    mounted() {
      console.log('AppHome mounted:', {
        route: this.$route.name,
        quotes: this.quotes,
        question: this.question
      });
    },
    methods: {
      async handleSubmit(query) {
        this.isLoading = true
        this.error = ''
  
        try {
          const response = await axios.post(`${import.meta.env.VITE_API_ENDPOINT}/quote`, { query })
          if (!response.data.quotes || response.data.quotes.length === 0) {
            throw new Error('No quotes received')
          }
          this.quotes = response.data.quotes
          this.question = query
        } catch (error) {
          console.error('Error fetching quote:', error)
          this.error = error.response?.data?.error ?? 'An unexpected error occurred. Please try again later.'
        } finally {
          this.isLoading = false
        }
      },
      resetQuery() {
        console.log('resetQuery called:', {
          route: this.$route.name,
          quotes: this.quotes,
          question: this.question
        });
        if (this.$route.name === 'Home' && !this.$router.savedState) {
          this.question = ''
          this.quotes = []
          this.error = ''
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .home {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 50px;
  }
  </style>