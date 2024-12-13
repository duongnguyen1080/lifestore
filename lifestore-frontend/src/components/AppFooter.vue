<template>
    <footer class="footer">
      <div class="footer-content">
        <p class="footer-text">
          <a href="https://www.newyorker.com/culture/annals-of-inquiry/when-philosophers-become-therapists" 
             target="_blank" 
             rel="noopener noreferrer" 
             class="counseling-link">Philosophical counseling</a> 
          helps people explore their values and find meaning in life through deep reflection.
        </p>
        <EmailSubscription />
      </div>
    </footer>
  </template>
  
  <script>
  import EmailSubscription from './EmailSubscription.vue'
  
  export default {
    name: 'AppFooter',
    components: {
      EmailSubscription
    }
  }
  </script>
  
  <style scoped>
.footer {
    width: 100%;
  display: flex;
  position: static;
  text-align: center;
  justify-content: center;
  margin-top: 0;
  margin-bottom: 1%;
  box-sizing: border-box;
}

.footer-content {
  max-width: 800px;
  width: 100%;
}

.footer-text {
  color: #000000;
  font-size: 14px;
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  line-height: 1.4;
  text-align: center;
  margin-bottom: 20px;
}

.counseling-link {
  color: #000000;
  text-decoration: underline;
  font-weight: inherit;
}

@media (max-width: 480px) {
  .footer {
    margin-top: 20px;
  }

  .footer-text {
    font-size: 16px;
  }
}
</style>