<template>
    <div class="loader-container">
      <mdicon name="diamond" :size="24" class="icon animated-icon" />
      <p class="loading-text">Working on it...</p>
    </div>
  </template>
  
  <script>
  import { mdiDiamondStone } from '@mdi/js'
  
  export default {
    name: 'DiamondLoader',
    data() {
      return {
        mdiDiamondStone
      }
    }
  }
  </script>
  
  <style scoped>
  .loader-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    height: 100vh;
    margin-top: 200px;
  }
  
  .icon {
    color: #a9d5fe;
    fill: #a9d5fe;
    font-size: 29px;
    width: 29px;
    height: 25px;
    margin-right: 0.5;
  }
  
  .animated-icon {
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
  }
  
  .loading-text {
    color: #898989;
    font-size: 14px;
    text-align: center;
  }
  </style>