<!--
  This is the secure login page for administrators.
-->
<script>
  import { goto } from '$app/navigation';

  let username = 'admin';
  let password = 'password123';
  let isLoading = false;
  let errorMessage = '';

  async function handleLogin() {
    isLoading = true;
    errorMessage = '';
    try {
      const response = await fetch('http://localhost:8080/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid username or password.');
      }
      
      // If login is successful, set a flag in sessionStorage and redirect.
      // This is a simple form of auth, real apps should use secure tokens.
      sessionStorage.setItem('isAdminLoggedIn', 'true');
      await goto('/admin/dashboard');

    } catch (error) {
      errorMessage = error.message;
    } finally {
      isLoading = false;
    }
  }
</script>

<svelte:head>
  <title>Admin Login | Campus Voice</title>
</svelte:head>

<div class="min-h-screen bg-gray-800 flex items-center justify-center p-4 font-sans">
  <div class="w-full max-w-md mx-auto bg-white p-8 rounded-xl shadow-lg">
    <header class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Administrator Portal</h1>
      <p class="mt-2 text-gray-600">Please log in to continue.</p>
    </header>
    <form on:submit|preventDefault={handleLogin} class="space-y-6">
      <div>
        <label for="username" class="block text-lg font-medium text-gray-700">Username</label>
        <input type="text" id="username" bind:value={username} required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      <div>
        <label for="password" class="block text-lg font-medium text-gray-700">Password</label>
        <input type="password" id="password" bind:value={password} required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
      </div>
      {#if errorMessage}
        <p class="text-red-500 text-sm">{errorMessage}</p>
      {/if}
      <div>
        <button type="submit" disabled={isLoading} class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300">
          {#if isLoading}Logging In...{:else}Log In{/if}
        </button>
      </div>
    </form>
  </div>
</div>

