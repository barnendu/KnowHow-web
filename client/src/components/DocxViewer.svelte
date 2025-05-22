<script>
    import { onMount } from 'svelte';
    import mammoth from 'mammoth';
  
    let fileContent = '';
    export let url=''
    onMount(async () => {
      const response = await fetch(url);
      const arrayBuffer = await response.arrayBuffer();
      const { value } = await mammoth.convertToHtml({ arrayBuffer });
      fileContent = value;
    });
  </script>
  
  <main>
    {#if fileContent}
      <div class="docx">{@html fileContent}</div>
    {:else}
      <p>Loading file...</p>
    {/if}
  </main>

  <style>
    .docx {
        overflow-x:auto; 
        height: calc(100vh - 80px);
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", Segoe UI Symbol, "Noto Color Emoji";
        font-size: small;
        padding: 15px;
        box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
    }
  </style>