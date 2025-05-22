<script>
    import { onMount } from 'svelte';
  
    let fileContent = '';
    export let url = '';
    onMount(async () => {
      const response = await fetch(url);
      fileContent = await response.text();
    });
  </script>
  
  <div class="txt">
    {#if fileContent}
      <pre>{fileContent}</pre>
    {:else}
      <p>Loading file...</p>
    {/if}
  </div>

  <style>
    .txt{
        overflow-x:auto; 
        height: calc(100vh - 80px);
        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
        padding: 15px;
     }
     .txt pre{
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", Segoe UI Symbol, "Noto Color Emoji";
        color: #000;
        background-color: #fff;
        font-size: small;
     }
  </style>