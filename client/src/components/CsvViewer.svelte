<script lang="ts">
    import { onMount } from 'svelte';
    import Papa from 'papaparse';
  
    /**
	 * @type {string | any[]}
	 */
    let tableColumns: string | any[] = [];
    let tableRows: string | any[] = [];
    export let url = '';
  
    onMount(async () => {
      Papa.parse(url, {
        download: true,
        complete: function(results) {
            tableColumns = results.data.slice(0,1)
            tableRows = results.data.slice(1)
	        }
        });
    });
  </script>
  
  <div class="csv-canvas">
    {#if tableColumns.length}
      <table class="csv">
        <thead>
          <tr>
            {#each Object.values(tableColumns[0]) as column}
              <th>{column}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each tableRows as row}
            {#if row != ''}
                <tr>
                {#each Object.values(row) as cell}
                    <td>{cell}</td>
                {/each}
                </tr>
            {/if}
          {/each}
        </tbody>
      </table>
    {:else}
      <p>Loading data...</p>
    {/if}
  </div>

  <style>
    .csv-canvas{
      overflow-x:auto;
      height: calc(100vh - 80px);
      box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
    }
    .csv {
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", Segoe UI Symbol, "Noto Color Emoji";
        border-collapse: collapse;
        font-size: small;
        width: 100%;
    }
    
    .csv td, .csv th {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .csv tbody{overflow-x:auto;}
    .csv tr:nth-child(even){background-color: #f2f2f2;}
    
    .csv tr:hover {background-color: #ddd;}
    
    .csv th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #04AA6D;
        color: white;
    }
 </style>