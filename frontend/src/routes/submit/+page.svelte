<!--
  This page contains the form for submitting a new anonymous report.
  It's designed to be straightforward and reassuring, guiding the user
  through the process of providing necessary details without causing alarm.
-->
<script>
  import { goto } from '$app/navigation';

  let report = {
    category: '',
    location: '',
    description: ''
  };
  let isLoading = false;
  let errorMessage = '';

  // Pre-defined categories for consistency in reporting.
  const categories = [
    "Campus Safety Concern",
    "Harassment or Bullying",
    "Mental Health Concern",
    "Academic Misconduct",
    "Maintenance Request",
    "Other"
  ];

  async function handleSubmit() {
    if (!report.category || !report.description.trim()) {
      errorMessage = "Please select a category and provide a description.";
      return;
    }
    isLoading = true;
    errorMessage = '';

    try {
      // The backend API is running on a different port, so we use the full URL.
      // In a production environment, this would be configured differently.
      const response = await fetch('http://localhost:8080/api/reports', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(report)
      });

      if (!response.ok) {
        throw new Error('An error occurred while submitting your report.');
      }

      const result = await response.json();
      
      // Store the received access code in sessionStorage to be displayed on the confirmation page.
      sessionStorage.setItem('reportAccessCode', result.accessCode);
      
      // Redirect to a dedicated confirmation page.
      await goto('/submit/success');

    } catch (error) {
      errorMessage = error.message;
    } finally {
      isLoading = false;
    }
  }
</script>

<svelte:head>
  <title>Submit a New Report | Campus Voice</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4 font-sans">
  <div class="w-full max-w-2xl mx-auto bg-white p-8 md:p-12 rounded-xl shadow-lg border border-gray-200">
    
    <!-- Back Navigation -->
    <a href="/" class="text-blue-600 hover:underline mb-8 inline-flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      Back to Home
    </a>
    
    <header class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Submit an Anonymous Report</h1>
      <p class="mt-2 text-gray-600">Your information is confidential and your submission is secure.</p>
    </header>

    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      
      <!-- Category Selection -->
      <div>
        <label for="category" class="block text-lg font-medium text-gray-700">Category</label>
        <select id="category" bind:value={report.category} required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow">
          <option value="" disabled>Select a category...</option>
          {#each categories as category}
            <option value={category}>{category}</option>
          {/each}
        </select>
      </div>

      <!-- Location Field -->
      <div>
        <label for="location" class="block text-lg font-medium text-gray-700">Location (Optional)</label>
        <p class="text-sm text-gray-500 mb-1">E.g., "Library, 3rd Floor" or "Near the main quad"</p>
        <input type="text" id="location" bind:value={report.location} placeholder="Enter a location" class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow" />
      </div>
      
      <!-- Description Field -->
      <div>
        <label for="description" class="block text-lg font-medium text-gray-700">Description</label>
        <p class="text-sm text-gray-500 mb-1">Please be as detailed as possible. Do not include any personal identifying information.</p>
        <textarea id="description" bind:value={report.description} rows="6" required class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow" placeholder="Describe the issue here..."></textarea>
      </div>
      
      {#if errorMessage}
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg" role="alert">
          <p>{errorMessage}</p>
        </div>
      {/if}

      <!-- Submit Button -->
      <div>
        <button type="submit" disabled={isLoading} class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-lg font-bold text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
          {#if isLoading}
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Submitting Securely...
          {:else}
            Submit Report Anonymously
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
