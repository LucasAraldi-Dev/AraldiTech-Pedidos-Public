<!-- AppMenuLayout.vue -->
<template>
    <div class="app-menu-layout">
      <router-view />
    </div>
  </template>
  
  <script>
  export default {
    name: 'AppMenuLayout',
  };
  </script>
  
  <style scoped>
  .app-menu-layout {
    background-color: #2c2c2c;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  </style>
  