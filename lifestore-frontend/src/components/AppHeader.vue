<template>
  <header class="header">
    <div class="card">
      <div class="header-content">
        <div class="logo">
          <mdicon name="diamond-stone" :size="24" />
        </div>
        <h1 class="text">Ask Philosophy</h1>
      </div>
    </div>
  </header>
</template>

<script setup>
</script>

<style scoped>
.header {
  position: absolute;
  top: -18px;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo {
  margin-right: 0.5;
  color: #a9d5fe;
  fill: #a9d5fe;
  font-size: 29px;
  width: 29px;
  height: 25px;
  padding-top: 8px;
}

.text {
  color: #030303;
  font-size: 20px;
  letter-spacing: -0.5px;
  line-height: 31px;
  padding-top: 15px;
}

@media (max-width: 480px) {
  .header {
    height: 50px;
  }

  .text {
    font-size: 20px;
    line-height: 26px;
  }

  .logo {
    margin-right: 8px;
  }
}

@media (max-width: 320px) {
  .text {
    font-size: 18px;
    line-height: 24px;
  }

  .logo {
    transform: scale(0.9);
  }
}
</style>