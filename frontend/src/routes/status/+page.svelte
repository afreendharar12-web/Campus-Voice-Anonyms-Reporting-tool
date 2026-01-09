<!--
  This page displays the status of a submitted report.
  It fetches the data from the backend using the access code
  and presents the report details and any updates in a clear timeline format.
-->
<script>
  import { onMount } from 'svelte';

  let accessCode = '';
  let reportData = null;
  let isLoading = true;
  let errorMessage = '';

  onMount(async () => {
    accessCode = sessionStorage.getItem('reportAccessCode') || '';
    if (!accessCode) {
      errorMessage = "No access code found. Please go back to the home page and enter your code.";
      isLoading = false;
      return;
    }
    await fetchReportStatus();
  });

  async function fetchReportStatus() {
    isLoading = true;
    errorMessage = '';
    try {
      const response = await fetch(`http://localhost:8080/api/reports/${accessCode}`);
      
      if (response.status === 404) {
        throw new Error("No report found with that access code. Please check the code and try again.");
      }
      if (!response.ok) {
        throw new Error("An error occurred while fetching your report.");
      }
      
      reportData = await response.json();
    } catch (error) {
      errorMessage = error.message;
      reportData = null;
    } finally {
      isLoading = false;
    }
  }

  function getStatusColor(status) {
    switch(status.toLowerCase()) {
      case 'new': return 'bg-blue-100 text-blue-800';
      case 'received': return 'bg-yellow-100 text-yellow-800';
      case 'under investigation': return 'bg-purple-100 text-purple-800';
      case 'resolved': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  function formatTimestamp(dateString) {
    return new Date(dateString).toLocaleString('en-US', {
      dateStyle: 'long',
      timeStyle: 'short'
    });
  }
</script>

<svelte:head>
  <title>Report Status | Campus Voice</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 p-4 sm:p-6 md:p-8 font-sans">
  <div class="max-w-4xl mx-auto">
    
    <!-- Back Navigation -->
    <a href="/" class="text-blue-600 hover:underline mb-8 inline-flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      Back to Home
    </a>

    {#if isLoading}
      <div class="text-center p-12">
        <p class="text-lg text-gray-600">Loading Report Status...</p>
      </div>
    {:else if errorMessage}
      <div class="bg-white p-8 rounded-xl shadow-lg border border-gray-200 text-center">
        <h2 class="text-2xl font-bold text-red-600 mb-4">Error</h2>
        <p class="text-gray-700">{errorMessage}</p>
      </div>
    {:else if reportData}
      <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <header class="bg-gray-50 p-6 border-b border-gray-200">
          <div class="flex flex-col sm:flex-row justify-between sm:items-center">
            <div>
              <h1 class="text-2xl font-bold text-gray-800">Report Status</h1>
              <p class="text-sm text-gray-500 mt-1">Your Access Code: <span class="font-mono">{accessCode}</span></p>
            </div>
            <div class="mt-4 sm:mt-0">
              <span class="text-sm font-bold py-1 px-3 rounded-full {getStatusColor(reportData.report.status)}">
                {reportData.report.status.toUpperCase()}
              </span>
            </div>
          </div>
        </header>

        <div class="p-6">
          <!-- Original Report Details -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Your Original Report</h2>
            <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 space-y-3">
              <p><strong class="font-medium text-gray-600">Submitted:</strong> {formatTimestamp(reportData.report.created_at)}</p>
              <p><strong class="font-medium text-gray-600">Category:</strong> {reportData.report.category}</p>
              {#if reportData.report.location}
                <p><strong class="font-medium text-gray-600">Location:</strong> {reportData.report.location}</p>
              {/if}
              <p class="pt-2 text-gray-700 whitespace-pre-wrap"><strong class="font-medium text-gray-600">Description:</strong><br>{reportData.report.description}</p>
            </div>
          </div>
          
          <!-- Updates Timeline -->
          <div>
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Status History & Updates</h2>
            {#if reportData.updates.length === 0}
              <p class="text-gray-600">No updates from the administration yet. Please check back later.</p>
            {:else}
              <ol class="relative border-l border-gray-200">                  
                {#each reportData.updates as update, i}
                  <li class="mb-10 ml-4">
                    <div class="absolute w-3 h-3 bg-gray-400 rounded-full mt-1.5 -left-1.5 border border-white"></div>
                    <time class="mb-1 text-sm font-normal leading-none text-gray-500">{formatTimestamp(update.created_at)}</time>
                    <h3 class="text-lg font-semibold text-gray-900">Status changed to: {update.new_status}</h3>
                    <p class="text-base font-normal text-gray-600">{update.message}</p>
                  </li>
                {/each}
              </ol>
            {/if}
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
