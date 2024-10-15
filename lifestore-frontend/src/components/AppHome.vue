<template>
    <div class="home">
    <QueryCard 
      v-if="!quote"
      :isLoading="isLoading"
      :error="error"
      :question="question"
      @submit="handleSubmit"
    />
    <ShowQuote 
      v-else
      :quote="quote"
      :userQuestion="question"
      @learnMore="openLearnMore"
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
        quote: '',
        isLoading: false,
        error: ''
      }
    },
    methods: {
      async handleSubmit(query) {
        this.isLoading = true
        this.error = ''
  
        try {
          const response = await axios.post('https://ask-philosophy-mvz8q4mfp-duongnguyen1080s-projects.vercel.app/api/quote', { query })
          this.quote = response.data.quote
          this.question = query
        } catch (error) {
          console.error('Error fetching quote:', error)
          this.error = error.response?.data?.error ?? 'An unexpected error occurred. Please try again later.'
        } finally {
          this.isLoading = false
        }
      },
      resetQuery() {
        this.question = ''
        this.quote = ''
        this.error = ''
      },
      openLearnMore() {
        const [quoteText, quoteAuthor] = this.quote.split('-').map(s => s.trim())
        this.$router.push({
          name: 'LearnMore',
          params: {
            authorInfo: quoteAuthor,
            userQuestion: this.question,
            quote: quoteText.replace(/^"|"$/g, '')
          }
        })
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