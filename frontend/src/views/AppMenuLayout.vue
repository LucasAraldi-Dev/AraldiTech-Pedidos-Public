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
    width: 100%;
    overflow-x: hidden;
  }
  
  /* Responsividade para diferentes dispositivos */
  @media (max-width: 1024px) {
    .app-menu-layout {
      padding: 10px;
    }
  }
  
  @media (max-width: 768px) {
    .app-menu-layout {
      padding: 5px;
    }
  }
  
  @media (max-width: 480px) {
    .app-menu-layout {
      padding: 0;
    }
  }
  </style>
  