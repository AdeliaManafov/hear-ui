<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="error-code">404</h1>
      <h2 class="error-title">{{ $t('not_found.message') }}</h2>
      <router-link to="/" class="home-link">
        <button class="primary-button">
          {{ $t('not_found.home') }}
        </button>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 Not Found page component
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  color: var(--primary-color, #3b82f6);
  margin: 0;
  line-height: 1;
}

.error-title {
  font-size: 2rem;
  color: var(--text-color, #1f2937);
  margin: 1rem 0;
}

.error-message {
  font-size: 1.125rem;
  color: var(--text-muted, #6b7280);
  margin-bottom: 2rem;
}

.home-link {
  text-decoration: none;
}

.primary-button {
  background-color: var(--primary-color, #3b82f6);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary-button:hover {
  background-color: var(--primary-hover, #2563eb);
}
</style>