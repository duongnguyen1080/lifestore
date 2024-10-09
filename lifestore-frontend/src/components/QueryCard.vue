<template>
  <div class="query-card">
    <h2>{{ question || "What burdens you today?" }}</h2>
    <form @submit.prevent="handleSubmit" class="query-form">
      <input
        v-model="query"
        type="text"
        :placeholder="question ? 'Type your question here' : 'Type your question here'"
        class="question-input"
        :disabled="isLoading"
        @keyup.enter="handleSubmit"
      />
      <mdicon 
        name="send"
        v-if="query.length >= 5 && !isLoading" 
        @click="handleSubmit" 
        class="send-icon"
      />
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'QueryCard',
  props: {
    isLoading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    question: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      query: ''
    }
  },
  methods: {
    handleSubmit() {
      if (this.query.length < 3 || this.isLoading) return
      this.$emit('submit', this.query)
    }
  }
}
</script>

<style scoped>
.query-card {
  width: 100%;
  max-width: 600px;
  margin: 200px auto 0;
  padding: 0 20px;
  box-sizing: border-box;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #030303;
  text-align: center;
}

.query-form {
  position: relative;
  display: flex;
  align-items: center;
}

.question-input {
  width: 100%;
  padding: 10px;
  padding-right: 50px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.send-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 12px;
  color: #7d7e80; 
}

.error-message {
  color: red;
  margin-top: 10px;
}

@media (max-width: 480px) {
  .query-card {
    margin-top: 40px;
  }
  
  h2 {
    font-size: 20px;
  }

  .question-input {
    font-size: 14px;
  }
}
</style>