<script>
    import { onMount } from 'svelte';
    import * as XLSX from 'xlsx';
  
    /**
	 * @type {string | any[]}
	 */
    let tableData = [];
    export let url = '';
  
    onMount(async () => {
      const response = await fetch(url);
      const arrayBuffer = await response.arrayBuffer();
      const workbook = XLSX.read(arrayBuffer, { type: 'array' });
      const worksheet = workbook.Sheets[workbook.SheetNames[0]];
      tableData = XLSX.utils.sheet_to_json(worksheet);
    });
  </script>
  
  <div class="xlsx-canvas">
    {#if tableData.length}
      <table class="xlsx">
        <thead>
          <tr>
            {#each Object.keys(tableData[0]) as column}
              <th>{column}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each tableData as row}
            <tr>
              {#each Object.values(row) as cell}
                <td>{cell}</td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <p>Loading data...</p>
    {/if}
    </div>

  <style>
    .xlsx-canvas{
      overflow-x:auto;
      height: calc(100vh - 80px);
      box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;

    }
    .xlsx {
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", Segoe UI Symbol, "Noto Color Emoji";
        border-collapse: collapse;
        font-size: small;
        width: 100%;
        
    }
    
    .xlsx td, .xlsx th {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .xlsx tbody{overflow-x:auto;}
    .xlsx tr:nth-child(even){background-color: #f2f2f2;}
    
    .xlsx tr:hover {background-color: #ddd;}
    
    .xlsx th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #04AA6D;
        color: white;
    }
 </style>