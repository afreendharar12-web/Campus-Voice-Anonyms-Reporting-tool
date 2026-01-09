<!-- 
  This is the main page for the Anonymous Reporting System.
  It serves as the entry point for students, allowing them to either
  submit a new report or check the status of an existing one.
  The design is intentionally clean, calm, and reassuring to build trust.
-->
<script>
  import { goto } from '$app/navigation';

  let accessCode = '';
  let isLoading = false;
  let errorMessage = '';

  async function checkStatus() {
    if (!accessCode.trim()) {
      errorMessage = 'Please enter your access code.';
      return;
    }
    isLoading = true;
    errorMessage = '';
    
    // The access code is stored in a client-side store (sessionStorage)
    // to be retrieved on the status page. This is a simple way to pass
    // the code without exposing it in the URL.
    sessionStorage.setItem('reportAccessCode', accessCode.trim());
    
    // Navigate to the status page.
    await goto('/status');

    isLoading = false;
  }
</script>

<svelte:head>
  <title>Campus Voice | Anonymous Reporting</title>
  <meta name="description" content="A safe and anonymous way to report campus issues." />
  <script src="https://cdn.tailwindcss.com"></script>
</svelte:head>

<div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4 font-sans">
  <div class="w-full max-w-2xl mx-auto">
    
    <!-- Header Section -->
    <header class="text-center mb-12">
      <svg class="mx-auto h-16 w-16 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h1 class="text-4xl md:text-5xl font-bold text-gray-800">Campus Voice</h1>
      <p class="mt-3 text-lg text-gray-600">A Safe Space to Be Heard. Anonymously.</p>
    </header>

    <main class="grid grid-cols-1 md:grid-cols-2 gap-8">
      
      <!-- Card 1: Submit a New Report -->
      <div class="bg-white p-8 rounded-xl shadow-lg border border-gray-200 flex flex-col items-center text-center">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Have Something to Report?</h2>
        <p class="text-gray-600 mb-6">
          Submit a report about safety, maintenance, mental health, or harassment. Your submission is completely anonymous.
        </p>
        <a href="/submit" class="w-full text-center bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors duration-300 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
          Submit a New Report
        </a>
      </div>

      <!-- Card 2: Check an Existing Report -->
      <div class="bg-white p-8 rounded-xl shadow-lg border border-gray-200 flex flex-col items-center text-center">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Check on a Report</h2>
        <p class="text-gray-600 mb-6">
          Enter the unique access code you received when you submitted your report.
        </p>
        <form on:submit|preventDefault={checkStatus} class="w-full flex flex-col">
          <input
            type="text"
            bind:value={accessCode}
            placeholder="e.g., ocean-sun-123"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
            aria-label="Access Code"
          />
          {#if errorMessage}
            <p class="text-red-500 text-sm mt-2">{errorMessage}</p>
          {/if}
          <button
            type="submit"
            disabled={isLoading}
            class="w-full mt-4 bg-gray-700 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-800 transition-colors duration-300 shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            {#if isLoading}
              Checking...
            {:else}
              Check Status
            {/if}
          </button>
        </form>
      </div>
    </main>

    <!-- Footer with Anonymity Guarantee -->
    <footer class="text-center mt-12 text-gray-500">
      <p class="font-semibold">Your Anonymity is Guaranteed.</p>
      <p class="text-sm mt-1">We use a one-way hashing system. We cannot see your access code, and we do not track your IP address. We can never identify you.</p>
    </footer>

  </div>
</div>
