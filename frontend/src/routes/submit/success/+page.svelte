<!--
  This page is CRITICAL. It is shown only once after a successful submission.
  Its sole purpose is to display the unique access code to the user and
  stress the importance of saving it.
-->
<script>
  import { onMount } from 'svelte';

  let accessCode = '';

  onMount(() => {
    accessCode = sessionStorage.getItem('reportAccessCode') || '';
    // For security, we clear the code from storage after displaying it.
    // The user must copy it from this screen.
    sessionStorage.removeItem('reportAccessCode');
  });

  async function copyToClipboard() {
    try {
      await navigator.clipboard.writeText(accessCode);
      alert('Code copied to clipboard!');
    } catch (err) {
      alert('Failed to copy. Please copy it manually.');
    }
  }
</script>

<svelte:head>
  <title>Success! Save Your Code | Campus Voice</title>
</svelte:head>

<div class="min-h-screen bg-green-50 flex items-center justify-center p-4 font-sans">
  <div class="w-full max-w-xl mx-auto bg-white p-8 md:p-12 rounded-xl shadow-2xl border-2 border-green-600 text-center">
    
    <header class="mb-6">
       <svg class="mx-auto h-20 w-20 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h1 class="text-3xl font-bold text-gray-800 mt-4">Report Submitted Successfully!</h1>
    </header>

    <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4 rounded-lg text-left mb-6">
      <h2 class="font-bold text-xl">IMPORTANT: Save Your Access Code</h2>
      <p class="mt-2">This is the **only** time you will see this code. It is your unique and anonymous key to check the status of your report. We cannot recover it for you.</p>
    </div>

    <!-- The Access Code Display -->
    <div class="bg-gray-100 p-6 rounded-lg border border-gray-300 flex items-center justify-between space-x-4">
      <span class="text-2xl md:text-3xl font-mono font-bold text-gray-800 tracking-wider">
        {accessCode || 'Loading...'}
      </span>
      <button on:click={copyToClipboard} class="bg-gray-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-700 transition-colors" title="Copy to Clipboard">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
      </button>
    </div>
    <p class="text-sm text-gray-500 mt-2">Please copy this code and store it somewhere safe.</p>
    
    <div class="mt-8">
      <a href="/" class="w-full inline-block text-center bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors duration-300 shadow-md">
        Return to Home
      </a>
    </div>

  </div>
</div>
