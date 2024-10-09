<template>
    <div class="quote-card" v-if="quote">
    <div class="question-container">
      <h2 class="question-text">{{ userQuestion }}</h2>
      <mdicon
        name="pencil"
        :size="27"
        class="edit-icon"
        @click="$emit('editQuery')"
      />
    </div>
      <p class="quote-text">"{{ quoteText }}"</p>
      <p class="author-text">- {{ quoteAuthor }}</p>
      <button class="learn-more-btn" @click="$emit('learnMore')">Learn More</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ShowQuote',
    props: {
      quote: {
        type: String,
        required: true
      },
      userQuestion: {
        type: String,
        required: true
      }
    },
    computed: {
      quoteText() {
        return this.quote.split('-')[0].trim().replace(/^"|"$/g, '')
      },
      quoteAuthor() {
        return this.quote.split('-')[1]?.trim() || ''
      }
    }
  }
  </script>
  
  <style scoped>
  .quote-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    max-width: 600px;
    margin: 50px;
    position: relative;
  }
  
  .question-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .question-text {
    color: #000000;
    font-size: 18px;
    font-weight: 500;
    line-height: 22px;
    text-align: center;
    margin: 0;
  }
  
  .edit-icon {
    color: #a9d5fe;
    font-size: 15px;
    width: 20px;
    height: 17px;
    cursor: pointer;
    margin-left: 2px;
    margin-bottom: 12px;
  }
  
  .quote-text {
    color: #1f2937;
    font-size: 18px;
    font-style: italic;
    line-height: 23px;
    text-align: center;
    margin-bottom: 10px;
  }
  
  .author-text {
    color: #1f2937;
    font-size: 16px;
    line-height: 24px;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .learn-more-btn {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #030303;
    border: none;
    border-radius: 4px;
    color: #ffffff;
    font-size: 16px;
    line-height: 24px;
    text-align: center;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .learn-more-btn:hover {
    background-color: #e5e7eb;
  }
  </style>