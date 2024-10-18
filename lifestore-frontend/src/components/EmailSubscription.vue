<template>
  <div class="email-subscription">
    <p class="subscription-text">Enter your email to receive philosophy literature suggestions and updates on the project.</p>
    <div class="input-container">
      <input 
        type="email" 
        v-model="email" 
        placeholder="Your Email Address" 
        class="email-input"
      />
      <button 
        @click="subscribe" 
        class="submit-button"
        :disabled="isLoading"
      >
        {{ isLoading ? 'Submitting...' : 'Submit' }}
      </button>
    </div>
    <p v-if="message" :class="['message', { 'error': isError }]">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';
const api = axios.create({
  baseURL: import.meta.env.VITE_API_ENDPOINT
});

export default {
  name: 'EmailSubscription',
  data() {
    return {
      email: '',
      isLoading: false,
      message: '',
      isError: false
    }
  },
  methods: {
    async subscribe() {
      if (!this.email) {
        this.showMessage('Please enter an email address.', true);
        return;
      }
      
      this.isLoading = true;
      try {
        const response = await api.post('/subscribe', { email: this.email });
        this.showMessage(response.data.message);
        this.email = '';
      } catch (error) {
        this.showMessage(error.response?.data?.message || 'An error occurred. Please try again.', true);
      } finally {
        this.isLoading = false;
      }
    },
    showMessage(msg, isError = false) {
      this.message = msg;
      this.isError = isError;
      setTimeout(() => {
        this.message = '';
        this.isError = false;
      }, 5000);
    }
  }
}
</script>
  
  <style scoped>
.email-subscription {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20;
  width: 100%;
}

.subscription-text {
  color: #000000;
  font-size: 14px;
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  line-height: 1.4;
  text-align: center;
  margin-bottom: 16px;
  max-width: 100%;
  padding: 0 20;
  box-sizing: border-box;
}

.input-container {
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 471px;
  padding: 0 20;
  box-sizing: border-box;
}

.email-input {
  flex-grow: 1;
  height: 36px;
  padding: 0 8px;
  border: 1px solid #505050;
  box-sizing: border-box;
  border-radius: 8px 0 0 8px;
  box-shadow: 0 0 10 rgba(0,0,0,0.1);
  background-color: #ffffff;
  color: #000000;
  font-size: 14px;
  font-family: "Roboto", sans-serif;
  line-height: 24px;
  outline: none;
}

.submit-button {
  cursor: pointer;
  width: 111px;
  height: 36px;
  padding: 0 8px;
  border: 0;
  box-sizing: border-box;
  border-radius: 0 6px 6px 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.16);
  background-color: #030303;
  color: #ffffff;
  font-size: 14px;
  font-family: "Roboto", sans-serif;
  line-height: 16px;
  outline: none;
}

.message {
  margin-top: 10;
  font-size: 14px;
  font-family: "Roboto", sans-serif;
}

.error {
  color: #ff0000;
}

@media (max-width: 480) {
  .input-container {
    flex-direction: column;
    align-items: stretch;
  }

  .email-input {
    border-radius: 8px;
    margin-bottom: 10;
  }

  .submit-button {
    width: 100%;
    border-radius: 8px;
  }

  .subscription-text {
    font-size: 16px;
  }
}
</style>