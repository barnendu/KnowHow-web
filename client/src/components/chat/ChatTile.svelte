<script lang="ts">

	interface Source {
		link: string;
		snippet: string;
    title:string;
	}

  export let sources:Source[] =[]; 

  const getDomainName = (url:string) => {
    const parsedUrl = new URL(url);
    let domain = parsedUrl.hostname;
    
    // Remove the "www." prefix if present
    if (domain.startsWith("www.")) {
      domain = domain.slice(4);
    }
    
    // Extract the top-level domain
    const parts = domain.split(".");
    if (parts.length > 1) {
      domain = parts.join(".");
    }
    
    return domain;
  }
</script>

<div class="grid grid-cols-3 gap-4">
    {#each sources as source}
      <div class="card">
        <div class="card-header">
        </div>
        <div class="card-body">
          <p>{source.title}</p>
        </div>
        <div class="card-footer">
          <img class="w-full object-cover comp-logo" src={`https://www.google.com/s2/favicons?sz=128&domain=${source.link}`} alt="Logo">
          <a class="text-gray-400 truncate comp-link" href={source.link} target="_blank" rel="noopener noreferrer">{getDomainName(source.link)}</a>
        </div>
      </div>
    {/each}
</div>

<style>
  .comp-logo{
    height:25px; 
    width:25px; 
    border-radius: 16px;
  }

  .comp-link{
    padding-left: 5px;
  }
  .card {
    border: 1px solid #ccc;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .card-header {
    background-color: #f5f5f5;
    padding: 0px;
    border-bottom: 1px solid #ccc;
  }

  .card-body {
    padding: 10px;
    font-size: 13px;
    max-height: 50%;
  }
  .card-body p{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .card-footer {
    display: flex;
    padding: 6px;
    border-top: 1px solid #ccc;
    text-align: right;
  }

</style>