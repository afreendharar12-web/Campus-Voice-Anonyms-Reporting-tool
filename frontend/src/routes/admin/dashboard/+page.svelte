<!--
  This is the main dashboard where administrators can view all reports,
  see details, and add updates.
-->
<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let reports = [];
  let isLoading = true;
  let selectedReport = null;
  
  let updateMessage = '';
  let newStatus = '';
  const possibleStatuses = ['New', 'Received', 'Under Investigation', 'Resolved'];

  onMount(async () => {
    // This is a simple client-side auth check. A real app would use secure tokens.
    if (sessionStorage.getItem('isAdminLoggedIn') !== 'true') {
      await goto('/admin/login');
      return;
    }
    await fetchReports();
  });

  async function fetchReports() {
    isLoading = true;
    try {
      const response = await fetch('http://localhost:8080/api/admin/reports');
      if (!response.ok) throw new Error('Failed to fetch reports.');
      reports = await response.json();
    } catch (error) {
      console.error(error);
      alert('Could not load reports. Please try again.');
    } finally {
      isLoading = false;
    }
  }
  
  function viewReport(report) {
    selectedReport = report;
    // Reset form fields when opening a new report
    newStatus = report.status;
    updateMessage = '';
  }

  async function handleUpdateSubmit() {
    if (!newStatus || !updateMessage.trim()) {
      alert('Please select a new status and enter a message for the reporter.');
      return;
    }
    
    try {
      const response = await fetch(`http://localhost:8080/api/admin/reports/${selectedReport.id}/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_status: newStatus, message: updateMessage }),
      });

      if (!response.ok) throw new Error('Failed to submit update.');
      
      alert('Update submitted successfully!');
      selectedReport = null; // Close modal
      await fetchReports(); // Refresh the list
    } catch (error) {
      alert(error.message);
    }
  }

  function formatTimestamp(dateString) {
    return new Date(dateString).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' });
  }
  
  function handleLogout() {
    sessionStorage.removeItem('isAdminLoggedIn');
    goto('/admin/login');
  }
</script>

<svelte:head>
  <title>Admin Dashboard | Campus Voice</title>
</svelte:head>

<div class="min-h-screen bg-gray-100 font-sans">
  <header class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">Reports Dashboard</h1>
      <button on:click={handleLogout} class="text-sm font-medium text-blue-600 hover:underline">Log Out</button>
    </div>
  </header>

  <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="bg-white p-6 rounded-xl shadow-lg">
      {#if isLoading}
        <p class="text-center text-gray-600">Loading reports...</p>
      {:else if reports.length === 0}
        <p class="text-center text-gray-600">No reports have been submitted yet.</p>
      {:else}
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-gray-50">
              <tr>
                <th class="p-4 font-semibold text-sm text-gray-600 uppercase tracking-wider">Date Submitted</th>
                <th class="p-4 font-semibold text-sm text-gray-600 uppercase tracking-wider">Category</th>
                <th class="p-4 font-semibold text-sm text-gray-600 uppercase tracking-wider">Description</th>
                <th class="p-4 font-semibold text-sm text-gray-600 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              {#each reports as report (report.id)}
                <tr class="hover:bg-gray-50 cursor-pointer" on:click={() => viewReport(report)} title="Click to view details and update">
                  <td class="p-4 whitespace-nowrap text-sm text-gray-700">{formatTimestamp(report.created_at)}</td>
                  <td class="p-4 text-sm text-gray-700">{report.category}</td>
                  <td class="p-4 text-sm text-gray-700 truncate max-w-md">{report.description}</td>
                  <td class="p-4 whitespace-nowrap">
                    <span class="text-xs font-semibold py-1 px-3 rounded-full bg-blue-100 text-blue-800">{report.status.toUpperCase()}</span>
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  </main>
</div>

<!-- Modal for Viewing and Updating a Report -->
{#if selectedReport}
  <div class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50" on:click|self={() => selectedReport = null}>
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col" on:click|stopPropagation>
      <header class="p-4 border-b flex justify-between items-center">
        <h2 class="text-xl font-bold text-gray-800">Report Details</h2>
        <button on:click={() => selectedReport = null} class="text-gray-500 hover:text-gray-800 text-2xl font-bold">&times;</button>
      </header>
      <div class="p-6 overflow-y-auto">
        <div class="space-y-3 mb-6 bg-gray-50 p-4 rounded-lg border">
          <p><strong>Report ID:</strong> <span class="font-mono text-sm text-gray-600">{selectedReport.id}</span></p>
          <p><strong>Submitted On:</strong> {formatTimestamp(selectedReport.created_at)}</p>
          <p><strong>Category:</strong> {selectedReport.category}</p>
          <p><strong>Location:</strong> {selectedReport.location || 'Not provided'}</p>
          <p class="whitespace-pre-wrap pt-2"><strong>Description:</strong><br>{selectedReport.description}</p>
        </div>
        <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-800">Add an Update</h3>
          <form on:submit|preventDefault={handleUpdateSubmit} class="space-y-4">
            <div>
              <label for="status" class="block font-medium text-gray-700">Change Status</label>
              <select bind:value={newStatus} id="status" required class="w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                <option disabled value="">Select new status</option>
                {#each possibleStatuses as status}<option value={status}>{status}</option>{/each}
              </select>
            </div>
            <div>
              <label for="message" class="block font-medium text-gray-700">Message for Reporter</label>
              <textarea bind:value={updateMessage} id="message" rows="4" required class="w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., We have dispatched a team to investigate. The student will see this message."></textarea>
            </div>
            <div class="flex justify-end pt-2">
              <button type="button" on:click={() => selectedReport = null} class="bg-gray-200 text-gray-800 font-bold py-2 px-4 rounded-lg hover:bg-gray-300 mr-2">Cancel</button>
              <button type="submit" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700">Submit Update</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
{/if}

